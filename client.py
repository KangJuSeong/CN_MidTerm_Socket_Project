from socket import *


IP = "127.0.0.1"
PORT = 10001
SIZE = 1024

def request_formating(method, body, url):
    return f"{method} / HTTP/1.1\r\nHost: {url}\r\nAccept: text/html\r\nContent-Type: text/html\r\nConnection: keep-alive\r\nContent-Length: {len(body)}\r\n\n{body}"

with socket(AF_INET, SOCK_STREAM) as client_socket:
    client_socket.connect((IP, PORT))  # 생성한 소켓에 HOST와 PORT 연결
    method = input("Input method (GET, POST, PUT, HEAD): ")
    url = input("Input URL : ")
    body = ''
    if method == 'POST' or method == 'PUT':
        body = input('Input Data : ')
    request = request_formating(method, body, url)

    client_socket.send(request.encode('utf-8'))

    response = client_socket.recv(SIZE).decode('utf-8')
    print(response)
    client_socket.close()