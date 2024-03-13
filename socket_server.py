import asyncio
import concurrent.futures
import struct

import aiohttp
import websockets

API_URL = "http://localhost:5000/get-data"
NUM_REQUESTS = 5000
CHUNK_SIZE = 500


async def fetch_data(url, req_num):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=20) as response:
            api_data = await response.json()
            return {"data": api_data, "req_num": req_num}


async def gather_tasks(start, end):
    return [fetch_data(API_URL, i)
            for i in range(start, end)]


def sort_result(item):
    return item['req_num']


async def thread_sort_results(results):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        ordered_results = list(executor.map(sort_result, results))

    sorted_results = [result for _, result in sorted(
        zip(ordered_results, results))]

    return sorted_results


async def package_results(sorted_results):
    return [sorted_results[i:i + CHUNK_SIZE]
            for i in range(0, len(sorted_results), CHUNK_SIZE)]


async def send_results(websocket, result):
    await websocket.send(f"{result}")


async def handle_websocket(websocket, path):
    try:
        results = []

        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")

            start_make_req = 0

            if message == "api":
                start_make_req += 1

                while (start_make_req < NUM_REQUESTS):
                    tasks = await gather_tasks(start_make_req, start_make_req + CHUNK_SIZE)

                    results = await asyncio.gather(*tasks)

                    sorted_results = await thread_sort_results(results)

                    package_data = await package_results(sorted_results)

                    await send_results(websocket, package_data)

                    start_make_req += CHUNK_SIZE

                await websocket.send(f"close_connection")

    except websockets.exceptions.ConnectionClosedOK:
        print("Connection closed by the client.")


if __name__ == "__main__":
    # Inicializar o loop de eventos asyncio
    loop = asyncio.get_event_loop()

    # Criar o servidor WebSocket
    start_server = websockets.serve(handle_websocket, "localhost", 8765)

    # Iniciar o servidor WebSocket
    loop.run_until_complete(start_server)
    print("WebSocket server started")

    # Manter o servidor em execução
    loop.run_forever()
