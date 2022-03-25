from socket import *


IP = "127.0.0.1"
PORT = 10000
SIZE = 1024

with socket(AF_INET, SOCK_STREAM) as client_socket:
    client_socket.connect((IP, PORT))  # 생성한 소켓에 HOST와 PORT 바인딩

    method = input("Input method (GET, POST, PUT, HEAD): ")
    url = input('Input URL : ')
    client_socket.send((method + ',' + url).encode('utf-8'))
    print("Sending Request to Server")

    data = client_socket.recv(SIZE).decode('utf-8')
    print("Response data : ", data)