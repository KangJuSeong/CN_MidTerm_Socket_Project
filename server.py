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


def find_http_method(line):
    line = line.split(' ')
    return line[0]
    
def response_formating(status_code, status_msg, body=''):
    date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.localtime(time.time()))
    return f"HTTP/1.1 {status_code} {status_msg}\r\nContent-Type: text/html\r\nConnection: keep-alive\r\nContent-Length: {len(body)}\r\nDate: {date}\r\n\n{body}"

def _response(status, body=''):
    if status == CONTINUE:
        return response_formating(STATUS_CODE[CONTINUE], STATUS_MESSAGE[CONTINUE], body)
    if status == OK:
        return response_formating(STATUS_CODE[OK], STATUS_MESSAGE[OK], body)
    elif status == CREATED:
        return response_formating(STATUS_CODE[CREATED], STATUS_MESSAGE[CREATED], body)
    elif status == BAD_REQUEST:
        return response_formating(STATUS_CODE[BAD_REQUEST], STATUS_MESSAGE[BAD_REQUEST], body)
    if status == NOT_FOUND:
        return response_formating(STATUS_CODE[NOT_FOUND], STATUS_MESSAGE[NOT_FOUND], body)
    

def router(url, method, body):
    if '/' in url:
        host, path = url.split('/')
        if host == HOST:
            if method == 'HEAD': return head()
            if path == 'index.html':
                if method == 'GET': return get()
                else: return _response(BAD_REQUEST)
            elif path == 'create':
                if method == 'POST': return post(body)
                else: return _response(BAD_REQUEST)
            elif path == 'update':
                if method == 'PUT': return put(body)
                else: return _response(BAD_REQUEST)
            else: return _response(NOT_FOUND)
        else:
            return ''
    else:
        return _response(NOT_FOUND)

def get():
    return _response(OK, body='index.html')

def head():
    return _response(CONTINUE) 

def post(body):
    k, v = body.split(':')
    if type(k) is str and type(v) is str:
        DB_DATA[k] = v
        return _response(CREATED, body=str(DB_DATA))
    else:
        return _response(BAD_REQUEST)

def put(body):
    k, v = body.split(':')
    if type(k) is str and type(v) is str:
        if k in DB_DATA.keys():
            DB_DATA[k] = v
            return _response(OK, body=str(DB_DATA))
        else:
            return _response(BAD_REQUEST, body='Not Exist Data')
    else:
        return _response(BAD_REQUEST)


with socket(AF_INET, SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))  # 생성한 소켓에 HOST와 PORT 바인딩
    server_socket.listen(1)  # 소켓 연결 대기 상태

    while True:
        client_socket, client_addr = server_socket.accept()  # 소켓이 연결 될 떄 client의 소켓과 주소 반환

        data = client_socket.recv(SIZE).decode('utf-8')  # client에서 보내는 데이터 받기
        print(data)
        data = data.split('\n')
        method = find_http_method(data[0])
        url = data[1][6:-1]
        body = data[-1]
        response = router(url, method, body)

        client_socket.send(response.encode('utf-8'))  # 데이터 인코딩하여 보내기