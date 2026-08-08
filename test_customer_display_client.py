import asyncio
import json

from websockets.asyncio.client import connect


SERVER_URL = "ws://127.0.0.1:8765"


async def main():

    print("Connecting to QuickBill Customer Display Server...")

    try:

        async with connect(SERVER_URL) as websocket:

            print("Connected successfully.")

            # Tell the server that this is a display client.
            await websocket.send(
                json.dumps(
                    {
                        "type": "hello",
                        "device": "Test Customer Display",
                    }
                )
            )

            print("Hello message sent.")

            # Wait for server response.
            response = await websocket.recv()

            print("Server response:")
            print(response)

            # Wait for future messages from the desktop.
            print("\nWaiting for broadcast messages...")
            print("Press Ctrl+C to stop.")

            while True:

                message = await websocket.recv()

                print("\nReceived:")
                print(message)

    except KeyboardInterrupt:

        print("\nClient stopped.")

    except Exception as exc:

        print(f"\nConnection error: {exc}")


if __name__ == "__main__":
    asyncio.run(main())