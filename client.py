from socket import *


IP = "127.0.0.1"
PORT = 10000
SIZE = 1024
test_case = [
    {'url': '127.0.0.1/index.html',
     'method': 'GET',
     'body': ''
    },
    {'url': '127.0.0.1/test.html',
     'method': 'GET',
     'body': ''
    },
    {'url': '127.0.0.1/',
     'method': 'HEAD',
     'body': ''
    },
    {'url': '127.0.0.1/create',
     'method': 'POST',
     'body': 'name:kangjuseong'
    },
    {'url': '127.0.0.1/create',
     'method': 'POST',
     'body': 'address:seongbukgu'
    },
    {'url': '127.0.0.1/create',
     'method': 'POST',
     'body': 'test'
    },
    {'url': '127.0.0.1/update',
     'method': 'PUT',
     'body': 'name:juseong-kang'
    },
    {'url': '127.0.0.1/update',
     'method': 'PUT',
     'body': 'grade:10'
    },
    {'url': '127.0.0.1/test',
     'method': 'POST',
     'body': 'test:test'
    }
]
def request_formating(method, body, url):
    return f"{method} / HTTP/1.1\r\nHost: {url}\r\nAccept: text/html\r\nContent-Type: text/html\r\nConnection: keep-alive\r\nContent-Length: {len(body)}\r\n\n{body}"

for test in test_case:
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect((IP, PORT))  # 생성한 소켓에 HOST와 PORT 연결
        method = test['method']
        url = test['url']
        body = test['body']
        request = request_formating(method, body, url)
        client_socket.send(request.encode('utf-8'))
        response = client_socket.recv(SIZE).decode('utf-8')
        print(response)
        print('------------------------------------------\n')
        client_socket.close()