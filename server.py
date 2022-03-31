from socket import *
import time
format = """HTTP/1.1 200 OK\n
            Content-Type: text/html\n
            ConnectionType: keep-alive\n
            Content-Length: 1\n
            Date: Wed, 10 Aug 2016 09:23:12 GMT\n\n

            body
        """

HOST = "127.0.0.1"
PORT = 10001
SIZE = 1024

CONTINUE = 0
OK = 1
CREATED = 2
BAD_REQUEST = 3
NOT_FOUND = 4
STATUS_CODE = ['100', '200', '201', '400', '404']
STATUS_MESSAGE = ['CONTINUE', 'OK', 'CREATED', 'BAD_REQUEST', 'NOT_FOUND']

DB_DATA = {}

def _response(status_code, status_msg, body=None):
    date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.localtime(time.time()))
    return f"HTTP/1.1 {status_code} {status_msg}\nContent-Type: text/html\nConnectionType: keep-alive\nContent-Length: {len(body)}\nDate: {date}\n\n{body}"

def router(url, method):
    host, path = url.split('/')

    if path == 'index.html': return get(method)
    # elif path == 'create': return post()
    # elif path == 'update': return put()
    # elif method == 'HEAD': return head()

def get(method):
    if method == 'GET':
        return _response(status_code=STATUS_CODE[OK],
                        status_msg=STATUS_MESSAGE[OK],
                        body='index.html')
    else:
        return _response(STATUS_CODE[BAD_REQUEST], STATUS_MESSAGE[BAD_REQUEST])

def post(method, k, v):
    if method == 'POST' and type(k) == 'str' and type(v) == 'str':
        DB_DATA[k] = v
        return _response(status_code=STATUS_CODE[CREATED],
                        status_msg=STATUS_MESSAGE[CREATED],
                        body=str(DB_DATA))
    else:
        return _response(STATUS_CODE[BAD_REQUEST], STATUS_MESSAGE[BAD_REQUEST])
    return response

# def put(url):
#     if url == HOST + '/update':
#         response = STATUS_CODE['OK']
#     return response


# def head(url):
#     if url == HOST + '/option':
#         response = STATUS_CODE['BAD REQUEST']
#     return response

with socket(AF_INET, SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))  # 생성한 소켓에 HOST와 PORT 바인딩
    server_socket.listen(1)  # 소켓 연결 대기 상태
    print("소켓이 대기중 입니다...")

    while True:
        client_socket, client_addr = server_socket.accept()  # 소켓이 연결 될 떄 client의 소켓과 주소 반환

        data = client_socket.recv(SIZE).decode('utf-8').split(',')  # client에서 보내는 데이터 받기
        method, url = data[0], data[1]
        body = data[2]
        response = router(url, method, body)
        client_socket.send(response.encode('utf-8'))  # 데이터 인코딩하여 보내기