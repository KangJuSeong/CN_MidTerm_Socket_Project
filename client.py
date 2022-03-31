from socket import *

format = """POST / HTTP/1.1\n
            Host: 127.0.0.1:10000
            Accept: text/html
            Content-Type: text/html\n
            ConnectionType: keep-alive\n
            Content-Length: 1\n\n

            body
        """

IP = "127.0.0.1"
PORT = 10001
SIZE = 1024

def request():
    return 1

with socket(AF_INET, SOCK_STREAM) as client_socket:
    client_socket.connect((IP, PORT))  # 생성한 소켓에 HOST와 PORT 연결
    method = input("Input method (GET, POST, PUT, HEAD): ")
    url = input('Input URL : ')
    body = input('Input Data' : ')

    client_socket.send((method + ',' + url + ',' + body).encode('utf-8'))

    data = client_socket.recv(SIZE).decode('utf-8')
    print(data)
    client_socket.close()