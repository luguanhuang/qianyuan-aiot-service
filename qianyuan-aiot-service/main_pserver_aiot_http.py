

from services.http.server import init_activemq
from services.http.server import htttp_start

def start():
    # 启动http服务
    init_activemq()
    htttp_start()
    # 启动mqtt服务
    # pass

if __name__ == "__main__":
    start()