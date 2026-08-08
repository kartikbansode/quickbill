import json
import threading
from typing import Optional, Set

try:
    from websockets.sync.server import serve
except ImportError:
    serve = None


class CustomerDisplayServer:
    """
    Optional WebSocket server for the QuickBill Android
    customer display.

    Android is only a customer-display client.

    The desktop QuickBill application remains fully
    functional if:
        - Android is disconnected
        - Android crashes
        - Wi-Fi/LAN fails
        - the display server fails
        - a client sends invalid data

    Android never controls or approves a desktop sale.
    """

    PROTOCOL_VERSION = 2

    def __init__(self, host="0.0.0.0", port=8765):

        self.host = host
        self.port = port

        self._thread: Optional[threading.Thread] = None
        self._server = None

        self._clients: Set = set()
        self._lock = threading.Lock()

        self._running = False
        self._available = False

        self._last_state = None

        self._status_callback = None

        self._stop_requested = False

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

        self._thread = threading.Thread(
            target=self._run_server,
            name="QuickBill-CustomerDisplay",
            daemon=True,
        )

        self._thread.start()

    # =========================================================
    # STOP
    # =========================================================

    def stop(self):

        self._stop_requested = True

        server = self._server

        if server is not None:

            try:
                server.shutdown()

            except Exception as exc:

                print(
                    "[CustomerDisplay] "
                    f"Shutdown warning: {exc}"
                )

        thread = self._thread

        if (
            thread is not None
            and thread.is_alive()
            and thread is not threading.current_thread()
        ):

            thread.join(timeout=5)

        self._running = False
        self._server = None

        with self._lock:

            clients = list(self._clients)
            self._clients.clear()

        for websocket in clients:

            try:
                websocket.close()

            except Exception:
                pass

        self._set_available(False)

    # =========================================================
    # SERVER THREAD
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

                self._set_available(True)

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

            self._set_available(False)

    # =========================================================
    # CLIENT HANDLER
    # =========================================================

    def _client_handler(self, websocket):

        with self._lock:
            self._clients.add(websocket)

        print(
            "[CustomerDisplay] "
            "Android display connected"
        )

        try:

            # Send the latest state immediately when
            # Android connects or reconnects.

            last_state = self.get_last_state()

            if last_state is not None:

                self._send(
                    websocket,
                    last_state,
                )

            while True:

                try:

                    raw_message = websocket.recv()

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
                self._clients.discard(websocket)

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

            message = json.loads(raw_message)

        except (TypeError, ValueError):

            return

        if not isinstance(message, dict):

            return

        message_type = message.get("type")

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
    # BROADCAST
    # =========================================================

    def broadcast(self, message):

        if not isinstance(message, dict):

            return False

        # Always remember the newest state.

        self._last_state = message

        if not self._running:

            return False

        with self._lock:

            clients = list(self._clients)

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

                dead_clients.append(websocket)

        if dead_clients:

            with self._lock:

                for websocket in dead_clients:

                    self._clients.discard(websocket)

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
        """
        Send the current live bill to Android.

        This is the main customer-display event.
        """

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
                        item.get("barcode", "")
                    ),
                    "sku": str(
                        item.get("sku", "")
                    ),
                    "name": str(
                        item.get("name", "")
                    ),
                    "brand": str(
                        item.get("brand", "")
                    ),
                    "category": str(
                        item.get("category", "")
                    ),
                    "qty": int(
                        item.get("qty", 0)
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
                        item.get("total", 0)
                    ),
                    "gst": float(
                        item.get("gst", 0)
                    ),
                }
            )

        message = {
            "type": "bill_update",
            "bill_no": str(bill_no),
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
            "cashier": str(cashier),
            "items": normalized_items,
            "subtotal": float(subtotal),
            "tax": float(tax),
            "discount": float(discount),
            "total": float(total),
            "payment": {
                "status": "pending",
                "mode": None,
            },
        }

        return self.broadcast(message)

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
        """
        Notify Android that the payment screen has started.

        QR is optional and should normally only be supplied
        for UPI payments.
        """

        mode = str(mode or "").strip()

        payment = {
            "status": "started",
            "mode": mode,
            "total": float(total),
            "qr": {
                "enabled": False,
            },
        }

        if mode.upper() == "UPI":

            if isinstance(qr, dict):

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
                }

            else:

                payment["qr"] = {
                    "enabled": True,
                    "amount": float(total),
                }

        self.broadcast(
            {
                "type": "payment_started",
                "bill_no": str(bill_no),
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
        """
        Notify Android that payment is waiting.

        This is particularly useful for UPI.
        """

        mode = str(mode or "").strip()

        payment = {
            "status": "pending",
            "mode": mode,
            "total": float(total),
        }

        if mode.upper() == "UPI":

            payment["qr"] = (
                qr
                if isinstance(qr, dict)
                else {
                    "enabled": True,
                    "amount": float(total),
                }
            )

        else:

            payment["qr"] = {
                "enabled": False,
            }

        self.broadcast(
            {
                "type": "payment_pending",
                "bill_no": str(bill_no),
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
        """
        Notify Android that payment was completed.

        This is generated by the desktop application.
        Android does not approve payment.
        """

        self.broadcast(
            {
                "type": "payment_completed",
                "bill_no": str(bill_no),
                "payment": {
                    "status": "completed",
                    "mode": mode,
                    "total": float(total),
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
        """
        Notify Android that payment was cancelled.
        """

        self.broadcast(
            {
                "type": "payment_cancelled",
                "bill_no": str(bill_no),
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
        """
        Notify Android that the complete desktop sale
        has successfully finished.
        """

        self.broadcast(
            {
                "type": "sale_completed",
                "bill_no": str(bill_no),
                "payment": {
                    "status": "completed",
                    "mode": mode,
                    "total": float(total),
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
        """
        Reset Android to a fresh bill.
        """

        if customer is None:

            customer = {
                "name": "Walk-in Customer",
                "mobile": "",
            }

        self.broadcast(
            {
                "type": "new_bill",
                "bill_no": str(bill_no),
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
                "cashier": str(cashier),
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
            separators=(",", ":"),
        )

        websocket.send(payload)

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

            return len(self._clients)

    def get_last_state(self):

        return self._last_state

    def _set_available(
        self,
        value,
    ):

        value = bool(value)

        changed = value != self._available

        self._available = value

        if not changed:

            return

        callback = self._status_callback

        if callback is None:

            return

        try:

            callback(value)

        except Exception:

            pass


# =============================================================
# GLOBAL INSTANCE
# =============================================================

customer_display = CustomerDisplayServer(
    host="0.0.0.0",
    port=8765,
)