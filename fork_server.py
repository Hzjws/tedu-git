from socket import *
import os,sys
import signal

def client_handler(c):
    print("处理子进程的请求",c.getpeername())
    try:
        while True:
            data=c.recv(1024)
            if not data:
                break
            print(data.decode())
            c.send("收到客户端请求".encode())
    except (KeyboardInterrupt,SystemError):
        sys.exit("客户端退出")
    except Exception as e:
        print("err:",e)
    c.close()
    sys.exit(0)

#创建套接字
host=""
port=8888
addr=(host,port)
s=socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(addr)
s.listen(5)

print("等待%d客户端连接"%os.getpid())

#在父进程中忽略子进程状态改变，子进程退出自动有系统处理
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

while True:
    try:
        c,addr=s.accept()
    except KeyboardInterrupt:
        sys.exit("服务器退出")
    except Exception as e:
        print("err:",e)
        continue

    #为客户端创建新的进程处理请求
    pid=os.fork()
    if pid==0:
        s.close()
        client_handler(c)
    else:
        c.close()
        continue