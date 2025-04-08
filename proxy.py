import socket
import threading

proxy_host = '127.0.0.1'  
proxy_port = 8888 # local proxy port

destination_host = 'example.com'
destination_port = 80

def handle_client(client_socket):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((destination_host, destination_port))

        def forward(source, destination):
            while True:
                data = source.recv(4096)
                if not data:
                    break
                destination.send(data)

     
        t1 = threading.Thread(target=forward, args=(client_socket, server_socket))
        t2 = threading.Thread(target=forward, args=(server_socket, client_socket))

        t1.start()
        t2.start()

        t1.join()
        t2.join()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        server_socket.close()

def start_proxy():
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Düzenlendi

    proxy_socket.bind((proxy_host, proxy_port))
    proxy_socket.listen(5)
    print(f"Proxy server listening on {proxy_host}:{proxy_port}")

    while True:
        client_socket, addr = proxy_socket.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_proxy()
