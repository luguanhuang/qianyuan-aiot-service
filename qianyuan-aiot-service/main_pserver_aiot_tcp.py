

from services.tcp.server import tcp_server

def start():
    # 启动tcp服务
    tcpserver = tcp_server()
    tcpserver.run()

    # pass

if __name__ == "__main__":
    start()