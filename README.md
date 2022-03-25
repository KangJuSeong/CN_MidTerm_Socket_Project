# CN_MidTerm_Socket_Project
## TCP 기반 소켓 프로그램을 작성하고 HTTP 프로토콜 방식 사용하여 Request/Response 구현

### 구조

- socket 통신을 이용하여 server와 client 간 통신 가능
- server에서 host와 port를 지정 후 server socket을 생성하여 대기
- client에서 server에서 사용한 host와 port를 통해 연결 된 socket 생성
- server에 연결된 client는 HTTP method와 url 주소를 보내서 응답 요청 (request)
- server에서는 client로부터 받은 HTTP method와 url을 검사하여 적절한 응답을 client로 전송 (response)
- client는 server로부터 받은 응답을 출력
- server에서 client로부터 잘못된 요청에 대한 응답은 400, 정상적인 요청에 대한 응답은 200(201)으로 응답
    
### 코드

1. server.py

    - socket 통신에 필요한 모듈 import
        ```python
        form socket import *
        ```


    - 각각의 GET, POST, PUT, HEAD 메소드에 맞는 함수 작성
    - 각각의 메소드에서 url을 검사하여 유효한 접근인지 판단
    - 만약 잘못된 접근일 경우 BAD REQUEST를 리턴

        ```python
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
        ```


    - host와 port, size를 변수에 저장
    - server에서 유효하다고 판단하기 위한 url 주소를 SERVER_URL에 저장
    - status code를 각각의 변수에 저장
        ```python
        HOST = "127.0.0.1"
        PORT = 10000
        SIZE = 1024
        SERVER_URL = "test.com"
        STATUS_CODE_OK = 'HTTP/200 OK'
        STATUS_CODE_BAD = 'HTTP/400 BAD REQUEST'
        STATUS_CODE_CREATED = 'HTTP/201 CREATED'
        ```


    - 지정한 HOST와 PORT를 이용하여 socket을 생성
    - `listen(1)` 메서드를 통해 socket 대기 상태
        ```python
        with socket(AF_INET, SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))  # 생성한 소켓에 HOST와 PORT 바인딩
            server_socket.listen(1)  # 소켓 연결 대기 상태
            print("소켓이 대기중 입니다...")
        ```
    

    - `accept()` 메소드를 통해 연결된 client의 socket과 address 저장
    - `recv(SIZE)` 메소드를 통해 client에서 보낸 HTTP method와 url을 가져온 후 저장
    - method에 맞는 HTTP method 함수 호출
    - `send(response)` 메소드를 통해 요청에 대한 알맞은 응답을 client로 전송
        ```python
            while True:
                client_socket, client_addr = server_socket.accept()  # 소켓이 연결 될 떄 client의 소켓과 주소 반환
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
        ```


2. client.py

    - socket 통신에 필요한 모듈 import
        ```python
        form socket import *
        ```


    - 소켓을 생성하고 IP와 PORT를 설정하여 server socket에 연결
        ```python
            while True:
                with socket(AF_INET, SOCK_STREAM) as client_socket:
                    client_socket.connect((IP, PORT))  # 생성한 소켓에 HOST와 PORT 연결
        ```


    - server로 요청할 HTTP method와 url을 입력 받기
    - 입력 받은 데이터를 인코딩 후 `send()` 메소드를 이용하여 서버로 요청을 전송
        ```python
                    method = input("Input method (GET, POST, PUT, HEAD): ")
                    url = input('Input URL : ')
                    client_socket.send((method + ',' + url).encode('utf-8'))
                    print("Sending Request to Server")
        ```

    
    - server로 부터 돌아온 응답을 `recv()` 메소드를 통해 받아오기
    - 받아온 response 출력 후 socket 종료
        ```python
                    data = client_socket.recv(SIZE).decode('utf-8')
                    print("Response data : ", data)
                    client_socket.close()
        ```



### 결과

