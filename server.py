from socket import *


HOST = "127.0.0.1"
PORT = 10000
SIZE = 1024
SERVER_URL = "test.com"
STATUS_CODE_OK = 'HTTP/200 OK'
STATUS_CODE_BAD = 'HTTP/400 BAD REQUEST'
STATUS_CODE_CREATED = 'HTTP/201 CREATED' 

def get(url):
    if url == SERVER_URL:
        response = STATUS_CODE_OK
    else:
        response = STATUS_CODE_BAD
    return response

def post(url):
    if url == SERVER_URL + '/create':
        response = STATUS_CODE_CREATED
    else:
        response = STATUS_CODE_BAD
    return response

def head(url):
    if url == SERVER_URL + '/option':
        response = STATUS_CODE_OK
    else:
        response = STATUS_CODE_BAD
    return response

def put(url):
    if url == SERVER_URL + '/update':
        response = STATUS_CODE_OK
    else:
        response = STATUS_CODE_BAD
    return response


with socket(AF_INET, SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))  # 생성한 소켓에 HOST와 PORT 바인딩
    server_socket.listen(1)  # 소켓 연결 대기 상태
    print("소켓이 대기중 입니다...")

    while True:
        client_socket, client_addr = server_socket.accept()  # 실제 소켓 연결 시 반환되는 실제 통신용 연결된 소켓과 연결주소 할당
        print(str(client_addr), "에서 접속 완료!")

        data = client_socket.recv(SIZE).decode('utf-8').split(',')  # client에서 보내는 데이터 받기
        method, url = data[0], data[1]

        if method == 'GET':
            response = get(url)
        
        elif method == 'POST':
            response = post(url)

        elif method == 'HEAD':
            response = head(url)
        else:
            response = put(url)
        print(f"Request Method/URL : {method} {url} - {response}")
        client_socket.send(response.encode('utf-8'))  # 데이터 인코딩하여 보내기