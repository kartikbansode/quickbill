import json
import socket
import threading
from typing import Optional, Set

try:
    from websockets.sync.server import serve
except ImportError:
    serve = None


class CustomerDisplayServer:
    """
    QuickBill Customer Display server.

    Desktop remains the source of truth.

    WebSocket:
        8765

    UDP discovery:
        8766

    Android can discover the PC automatically on the
    same local network and then connect through WebSocket.
    """

    PROTOCOL_VERSION = 2

    DISCOVERY_PORT = 8766

    DISCOVERY_REQUEST = (
        "QUICKBILL_DISCOVER_V1"
    )

    def __init__(
        self,
        host="0.0.0.0",
        port=8765,
    ):

        self.host = host
        self.port = port

        self._thread: Optional[
            threading.Thread
        ] = None

        self._discovery_thread: Optional[
            threading.Thread
        ] = None

        self._server = None

        self._discovery_socket = None

        self._clients: Set = set()

        self._lock = threading.Lock()

        self._running = False
        self._available = False

        self._last_state = None

        self._status_callback = None

        self._stop_requested = False

        self._discovery_stop = threading.Event()

    # =========================================================
    # START
    # =========================================================

    def start(self):

        if self._running:
            return

        if serve is None:

            print(
                "[CustomerDisplay] "
                "websockets.sync.server is unavailable."
            )

            self._set_available(False)

            return

        self._stop_requested = False

        self._discovery_stop.clear()

        self._thread = threading.Thread(
            target=self._run_server,
            name="QuickBill-CustomerDisplay",
            daemon=True,
        )

        self._thread.start()

        # Start LAN discovery independently.
        self._discovery_thread = threading.Thread(
            target=self._run_discovery_server,
            name="QuickBill-CustomerDisplay-Discovery",
            daemon=True,
        )

        self._discovery_thread.start()

    # =========================================================
    # STOP
    # =========================================================

    def stop(self):

        self._stop_requested = True

        self._discovery_stop.set()

        # Stop WebSocket server.
        server = self._server

        if server is not None:

            try:
                server.shutdown()

            except Exception as exc:

                print(
                    "[CustomerDisplay] "
                    f"Shutdown warning: {exc}"
                )

        # Stop discovery socket.
        discovery_socket = (
            self._discovery_socket
        )

        if discovery_socket is not None:

            try:
                discovery_socket.close()

            except Exception:
                pass

        thread = self._thread

        if (
            thread is not None
            and thread.is_alive()
            and thread is not threading.current_thread()
        ):

            thread.join(
                timeout=5
            )

        discovery_thread = (
            self._discovery_thread
        )

        if (
            discovery_thread is not None
            and discovery_thread.is_alive()
            and discovery_thread is not threading.current_thread()
        ):

            discovery_thread.join(
                timeout=2
            )

        self._running = False

        self._server = None
        self._discovery_socket = None

        with self._lock:

            clients = list(
                self._clients
            )

            self._clients.clear()

        for websocket in clients:

            try:
                websocket.close()

            except Exception:
                pass

        self._set_available(False)

    # =========================================================
    # WEBSOCKET SERVER
    # =========================================================

    def _run_server(self):

        try:

            with serve(
                self._client_handler,
                self.host,
                self.port,
            ) as server:

                self._server = server

                self._running = True

                self._set_available(
                    True
                )

                print(
                    "[CustomerDisplay] "
                    f"Server started on "
                    f"{self.host}:{self.port}"
                )

                server.serve_forever()

        except Exception as exc:

            if not self._stop_requested:

                print(
                    "[CustomerDisplay] "
                    f"Server stopped: {exc}"
                )

        finally:

            self._running = False

            self._server = None

            with self._lock:

                self._clients.clear()

            self._set_available(
                False
            )

    # =========================================================
    # UDP DISCOVERY SERVER
    # =========================================================

    def _run_discovery_server(self):

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
        )

        self._discovery_socket = sock

        try:

            sock.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_REUSEADDR,
                1,
            )

            sock.setsockopt(
                socket.SOL_SOCKET,
                socket.SO_BROADCAST,
                1,
            )

            sock.bind(
                (
                    "0.0.0.0",
                    self.DISCOVERY_PORT,
                )
            )

            sock.settimeout(
                1.0
            )

            print(
                "[CustomerDisplay] "
                f"Discovery server started on UDP "
                f"{self.DISCOVERY_PORT}"
            )

            while not self._discovery_stop.is_set():

                try:

                    data, address = (
                        sock.recvfrom(1024)
                    )

                except socket.timeout:

                    continue

                except OSError:

                    break

                request = (
                    data
                    .decode(
                        "utf-8",
                        errors="ignore",
                    )
                    .strip()
                )

                if request != self.DISCOVERY_REQUEST:

                    continue

                android_ip = address[0]

                desktop_ip = (
                    self._get_ip_for_client(
                        android_ip
                    )
                )

                response = {
                    "type": (
                        "quickbill_discovery_response"
                    ),
                    "service": (
                        "QuickBill Customer Display"
                    ),
                    "ip": desktop_ip,
                    "port": self.port,
                    "version": self.PROTOCOL_VERSION,
                }

                payload = json.dumps(
                    response,
                    separators=(
                        ",",
                        ":",
                    ),
                ).encode(
                    "utf-8"
                )

                try:

                    sock.sendto(
                        payload,
                        address,
                    )

                    print(
                        "[CustomerDisplay] "
                        f"Discovery response sent to "
                        f"{android_ip} -> "
                        f"{desktop_ip}:{self.port}"
                    )

                except OSError:
                    pass

        except Exception as exc:

            if not self._stop_requested:

                print(
                    "[CustomerDisplay] "
                    f"Discovery server error: {exc}"
                )

        finally:

            try:
                sock.close()

            except Exception:
                pass

            self._discovery_socket = None

    # =========================================================
    # FIND CORRECT LAN IP
    # =========================================================

    @staticmethod
    def _get_ip_for_client(
        client_ip,
    ):

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
        )

        try:

            sock.connect(
                (
                    client_ip,
                    1,
                )
            )

            return sock.getsockname()[0]

        except Exception:

            try:

                hostname = socket.gethostname()

                return socket.gethostbyname(
                    hostname
                )

            except Exception:

                return "127.0.0.1"

        finally:

            sock.close()

    # =========================================================
    # CLIENT HANDLER
    # =========================================================

    def _client_handler(
        self,
        websocket,
    ):

        with self._lock:

            self._clients.add(
                websocket
            )

        print(
            "[CustomerDisplay] "
            "Android display connected"
        )

        try:

            # Send latest state immediately.
            last_state = (
                self.get_last_state()
            )

            if last_state is not None:

                self._send(
                    websocket,
                    last_state,
                )

            while True:

                try:

                    raw_message = (
                        websocket.recv()
                    )

                except Exception:

                    break

                if raw_message is None:

                    break

                self._handle_client_message(
                    websocket,
                    raw_message,
                )

        except Exception as exc:

            if not self._stop_requested:

                print(
                    "[CustomerDisplay] "
                    f"Client error: {exc}"
                )

        finally:

            with self._lock:

                self._clients.discard(
                    websocket
                )

            try:

                websocket.close()

            except Exception:
                pass

            print(
                "[CustomerDisplay] "
                "Android display disconnected"
            )

    # =========================================================
    # CLIENT MESSAGES
    # =========================================================

    def _handle_client_message(
        self,
        websocket,
        raw_message,
    ):

        try:

            message = json.loads(
                raw_message
            )

        except (
            TypeError,
            ValueError,
        ):

            return

        if not isinstance(
            message,
            dict,
        ):

            return

        message_type = (
            message.get("type")
        )

        if message_type == "hello":

            self._send(
                websocket,
                {
                    "type": "hello_ack",
                    "app": "QuickBill",
                    "server": "customer_display",
                    "version": self.PROTOCOL_VERSION,
                },
            )

        elif message_type == "ping":

            self._send(
                websocket,
                {
                    "type": "pong",
                },
            )

    # =========================================================
    # SEND
    # =========================================================

    def _send(
        self,
        websocket,
        message,
    ):

        payload = json.dumps(
            message,
            ensure_ascii=False,
            separators=(
                ",",
                ":",
            ),
        )

        websocket.send(
            payload
        )

    # =========================================================
    # BROADCAST
    # =========================================================

    def broadcast(
        self,
        message,
    ):

        if not isinstance(
            message,
            dict,
        ):

            return False

        self._last_state = message

        if not self._running:

            return False

        with self._lock:

            clients = list(
                self._clients
            )

        if not clients:

            return False

        dead_clients = []

        for websocket in clients:

            try:

                self._send(
                    websocket,
                    message,
                )

            except Exception:

                dead_clients.append(
                    websocket
                )

        if dead_clients:

            with self._lock:

                for websocket in dead_clients:

                    self._clients.discard(
                        websocket
                    )

        return True

    # =========================================================
    # BILL UPDATE
    # =========================================================

    def bill_update(
        self,
        bill_no,
        items=None,
        subtotal=0.0,
        tax=0.0,
        discount=0.0,
        total=0.0,
        customer=None,
        cashier="Admin",
    ):

        if items is None:
            items = []

        if customer is None:

            customer = {
                "name": "Walk-in Customer",
                "mobile": "",
            }

        normalized_items = []

        for item in items:

            normalized_items.append(
                {
                    "barcode": str(
                        item.get(
                            "barcode",
                            "",
                        )
                    ),

                    "sku": str(
                        item.get(
                            "sku",
                            "",
                        )
                    ),

                    "name": str(
                        item.get(
                            "name",
                            "",
                        )
                    ),

                    "brand": str(
                        item.get(
                            "brand",
                            "",
                        )
                    ),

                    "category": str(
                        item.get(
                            "category",
                            "",
                        )
                    ),

                    "qty": int(
                        item.get(
                            "qty",
                            0,
                        )
                    ),

                    "rate": float(
                        item.get(
                            "price",
                            item.get(
                                "selling_price",
                                0,
                            ),
                        )
                    ),

                    "amount": float(
                        item.get(
                            "total",
                            0,
                        )
                    ),

                    "gst": float(
                        item.get(
                            "gst",
                            0,
                        )
                    ),
                }
            )

        return self.broadcast(
            {
                "type": "bill_update",

                "bill_no": str(
                    bill_no
                ),

                "customer": {
                    "name": str(
                        customer.get(
                            "name",
                            "Walk-in Customer",
                        )
                    ),

                    "mobile": str(
                        customer.get(
                            "mobile",
                            "",
                        )
                    ),
                },

                "cashier": str(
                    cashier
                ),

                "items": normalized_items,

                "subtotal": float(
                    subtotal
                ),

                "tax": float(
                    tax
                ),

                "discount": float(
                    discount
                ),

                "total": float(
                    total
                ),

                "payment": {
                    "status": "pending",
                    "mode": None,
                },
            }
        )

    # =========================================================
    # PAYMENT STARTED
    # =========================================================

    def payment_started(
        self,
        bill_no,
        mode,
        total,
        qr=None,
    ):

        mode = str(
            mode or ""
        ).strip()

        payment = {
            "status": "started",
            "mode": mode,
            "total": float(
                total
            ),
            "qr": {
                "enabled": False,
            },
        }

        if mode.upper() == "UPI":

            if isinstance(
                qr,
                dict,
            ):

                payment["qr"] = {
                    "enabled": bool(
                        qr.get(
                            "enabled",
                            True,
                        )
                    ),

                    "upi_id": qr.get(
                        "upi_id",
                        "",
                    ),

                    "amount": float(
                        qr.get(
                            "amount",
                            total,
                        )
                    ),

                    "payload": qr.get(
                        "payload",
                        "",
                    ),

                    "merchant_name": qr.get(
                        "merchant_name",
                        "QuickBill",
                    ),
                }

            else:

                payment["qr"] = {
                    "enabled": True,
                    "amount": float(
                        total
                    ),
                }

        return self.broadcast(
            {
                "type": "payment_started",
                "bill_no": str(
                    bill_no
                ),
                "payment": payment,
            }
        )

    # =========================================================
    # PAYMENT PENDING
    # =========================================================

    def payment_pending(
        self,
        bill_no,
        mode,
        total,
        qr=None,
    ):

        mode = str(
            mode or ""
        ).strip()

        payment = {
            "status": "pending",
            "mode": mode,
            "total": float(
                total
            ),
        }

        if mode.upper() == "UPI":

            payment["qr"] = (
                qr
                if isinstance(
                    qr,
                    dict,
                )
                else {
                    "enabled": True,
                    "amount": float(
                        total
                    ),
                }
            )

        else:

            payment["qr"] = {
                "enabled": False,
            }

        return self.broadcast(
            {
                "type": "payment_pending",
                "bill_no": str(
                    bill_no
                ),
                "payment": payment,
            }
        )

    # =========================================================
    # PAYMENT COMPLETED
    # =========================================================

    def payment_completed(
        self,
        bill_no,
        mode,
        total,
    ):

        return self.broadcast(
            {
                "type": "payment_completed",
                "bill_no": str(
                    bill_no
                ),
                "payment": {
                    "status": "completed",
                    "mode": mode,
                    "total": float(
                        total
                    ),
                },
            }
        )

    # =========================================================
    # PAYMENT CANCELLED
    # =========================================================

    def payment_cancelled(
        self,
        bill_no,
        mode=None,
    ):

        return self.broadcast(
            {
                "type": "payment_cancelled",
                "bill_no": str(
                    bill_no
                ),
                "payment": {
                    "status": "cancelled",
                    "mode": mode,
                },
            }
        )

    # =========================================================
    # SALE COMPLETED
    # =========================================================

    def sale_completed(
        self,
        bill_no,
        mode,
        total,
    ):

        return self.broadcast(
            {
                "type": "sale_completed",
                "bill_no": str(
                    bill_no
                ),
                "payment": {
                    "status": "completed",
                    "mode": mode,
                    "total": float(
                        total
                    ),
                },
            }
        )

    # =========================================================
    # NEW BILL
    # =========================================================

    def new_bill(
        self,
        bill_no,
        customer=None,
        cashier="Admin",
    ):

        if customer is None:

            customer = {
                "name": "Walk-in Customer",
                "mobile": "",
            }

        return self.broadcast(
            {
                "type": "new_bill",
                "bill_no": str(
                    bill_no
                ),

                "customer": {
                    "name": str(
                        customer.get(
                            "name",
                            "Walk-in Customer",
                        )
                    ),

                    "mobile": str(
                        customer.get(
                            "mobile",
                            "",
                        )
                    ),
                },

                "cashier": str(
                    cashier
                ),

                "items": [],

                "subtotal": 0.0,
                "tax": 0.0,
                "discount": 0.0,
                "total": 0.0,

                "payment": {
                    "status": "idle",
                    "mode": None,
                },
            }
        )

    # =========================================================
    # STATUS
    # =========================================================

    def set_status_callback(
        self,
        callback,
    ):

        self._status_callback = callback

    def is_available(self):

        return self._available

    def connected_clients(self):

        with self._lock:

            return len(
                self._clients
            )

    def get_last_state(self):

        return self._last_state

    def _set_available(
        self,
        value,
    ):

        value = bool(value)

        changed = (
            value
            != self._available
        )

        self._available = value

        if not changed:

            return

        callback = (
            self._status_callback
        )

        if callback is None:

            return

        try:

            callback(
                value
            )

        except Exception:
            pass


# =============================================================
# GLOBAL INSTANCE
# =============================================================

customer_display = CustomerDisplayServer(
    host="0.0.0.0",
    port=8765,
)