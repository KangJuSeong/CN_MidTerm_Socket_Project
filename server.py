from socket import *
import time
from DBManager import DataBaseManager


HOST = "127.0.0.1"
PORT = 10000
SIZE = 1024

CONTINUE = 0
OK = 1
CREATED = 2
BAD_REQUEST = 3
NOT_FOUND = 4
STATUS_CODE = ['100', '200', '201', '400', '404']
STATUS_MESSAGE = ['CONTINUE', 'OK', 'CREATED', 'BAD_REQUEST', 'NOT_FOUND']


def find_http_method(line):
    line = line.split(' ')
    return line[0]
    
def response_formating(status_code, status_msg, body=''):
    date = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.localtime(time.time()))
    return f"HTTP/1.1 {status_code} {status_msg}\r\nContent-Type: text/html\r\nConnection: keep-alive\r\nContent-Length: {len(body)}\r\nDate: {date}\r\n\n{body}"

def response(status, body=''):
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
            if method == 'GET': return get()
            if path == 'create':
                if method == 'POST': return post(body)
                else: return response(BAD_REQUEST)
            elif path == 'update':
                if method == 'PUT': return put(body)
                else: return response(BAD_REQUEST)
            else: return response(NOT_FOUND)
        else:
            return ''
    else:
        return response(NOT_FOUND)

def get():
    dbm = DataBaseManager()
    res = dbm.selectDB()
    return response(OK, body=str(res))

def head():
    return response(CONTINUE) 

def post(body):
    body = body.split(':')
    if len(body) == 2:
        dbm = DataBaseManager()
        res = dbm.insertDB(body[0], body[1])
        if type(res) is not str:
            return response(CREATED, body=str(res))
        else:
            return response(BAD_REQUEST, body=res)
    else:
        return response(BAD_REQUEST)

def put(body):
    body = body.split(':')
    if len(body) == 2:
        dbm = DataBaseManager()
        res = dbm.updateDB(body[0], body[1])
        if type(res) is not str:
            return response(OK, body=str(res))
        else:
            return response(BAD_REQUEST, body=res)
    else:
        return response(BAD_REQUEST)


with socket(AF_INET, SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))  # ????????? ????????? HOST??? PORT ?????????
    server_socket.listen(1)  # ?????? ?????? ?????? ??????

    while True:
        client_socket, client_addr = server_socket.accept()  # ????????? ?????? ??? ??? client??? ????????? ?????? ??????

        data = client_socket.recv(SIZE).decode('utf-8')  # client?????? ????????? ????????? ??????
        print(data)
        print('------------------------------------------\n')
        data = data.split('\n')
        method = find_http_method(data[0])
        url = data[1][6:-1]
        body = data[-1]
        res = router(url, method, body)

        client_socket.send(res.encode('utf-8'))  # ????????? ??????????????? ?????????
