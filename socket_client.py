import asyncio

import websockets


async def send_receive_message(uri, message):
    async with websockets.connect(uri) as websocket:
        # Enviar mensagem para o servidor
        await websocket.send(message)
        print(f"Sent message: {message}")

        try:
            response = []
            while True:
                try:
                    response = await websocket.recv()

                    print(f"Received response: {response}")
                except websockets.exceptions.ConnectionClosedOK:
                    print("Connection closed by the server.")
                    break

                except websockets.exceptions.ConnectionClosedError as e:
                    print(f"Connection closed with error: {e}")
                    break

                finally:
                    if response == "close_connection":
                        break

        except Exception as e:
            print(f"Connection closed with error: {e}")
        finally:
            await websocket.close()

if __name__ == "__main__":
    # Endereço do servidor WebSocket (ajuste conforme necessário)
    server_uri = "ws://localhost:8765"

    # Mensagem a ser enviada ao servidor (ajuste conforme necessário)
    message_to_send = "api"

    # Inicializar o loop de eventos asyncio
    loop = asyncio.get_event_loop()

    # Executar a função de envio/recebimento de mensagens
    loop.run_until_complete(send_receive_message(server_uri, message_to_send))
