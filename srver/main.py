import asyncio
import ssl
import websockets

VALID_TOKEN = "my_secret_token"

async def process_data(data):
    for i in range(1, 6):
        chunk = f"Чанк {i} из обработанных данных для: {data}"
        await asyncio.sleep(1)
        yield chunk

async def handler(websocket, path):
    token = await websocket.recv()
    if token != VALID_TOKEN:
        await websocket.send("Аутентификация не удалась")
        await websocket.close()
        return
    else:
        await websocket.send("Аутентификация успешна")

    async for message in websocket:
        print(f"Получены данные от клиента: {message}")
        async for chunk in process_data(message):
            await websocket.send(chunk)
        await websocket.send("Обработка завершена")

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')

start_server = websockets.serve(handler, "0.0.0.0", 8765, ssl=ssl_context)

asyncio.get_event_loop().run_until_complete(start_server)
print("Сервер запущен на wss://0.0.0.0:8765")
asyncio.get_event_loop().run_forever()
