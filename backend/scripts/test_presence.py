import asyncio
import json
import sys
import websockets


async def login(email: str, password: str) -> str:
    """Hace login HTTP y devuelve el token."""
    import urllib.request
    import urllib.parse

    body = json.dumps({"email": email, "password": password}).encode()
    req = urllib.request.Request(
        "http://localhost:8000/api/v1/auth/login",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    return data["access_token"]


async def listen(name: str, ws):
    """Imprime todo lo que recibe."""
    try:
        async for raw in ws:
            print(f"[{name}] <- {raw}")
    except websockets.exceptions.ConnectionClosed:
        print(f"[{name}] connection closed")


async def main():
    # Login Alice y Bob
    alice_token = await login("alice@test.com", "alicepass1")
    bob_token = await login("bob@test.com", "bobpass12")

    alice_url = f"ws://localhost:8000/ws/presence?token={alice_token}"
    bob_url = f"ws://localhost:8000/ws/presence?token={bob_token}"

    async with websockets.connect(alice_url) as alice_ws, websockets.connect(bob_url) as bob_ws:
        # Tareas de escucha en paralelo
        alice_listener = asyncio.create_task(listen("alice", alice_ws))
        bob_listener = asyncio.create_task(listen("bob", bob_ws))

        await asyncio.sleep(1)
        print("\n--- Bob envía posición ---")
        await bob_ws.send(json.dumps({"type": "location", "lat": 40.4168, "lng": -3.7038}))

        await asyncio.sleep(1)
        print("\n--- Alice envía posición ---")
        await alice_ws.send(json.dumps({"type": "location", "lat": 41.3851, "lng": 2.1734}))

        await asyncio.sleep(1)
        print("\n--- Bob actualiza posición ---")
        await bob_ws.send(json.dumps({"type": "location", "lat": 40.5, "lng": -3.8}))

        await asyncio.sleep(1)
        print("\n--- Bob se desconecta ---")
        await bob_ws.close()

        await asyncio.sleep(1)
        alice_listener.cancel()
        bob_listener.cancel()


if __name__ == "__main__":
    asyncio.run(main())
