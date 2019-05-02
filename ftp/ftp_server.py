'''
ftp文件服务器
'''
from socket import *
import os,sys,time,signal

#文件库路径
file_path="/home/tarena/ftpFile/"
host='0.0.0.0'
port=8000
addr=(host,port)

#将文件服务器功能写在类中
class FtpServer(object):
    def __init__(self,connfd):
        self.connfd=connfd

    def do_list(self):
        file_list=os.listdir(file_path)
        if not file_list:
            self.connfd.send("文件库为空".encode())
            return
        else:
            self.connfd.send(b'ok')
            time.sleep(.1)

        files=''
        for file in file_list:
            if file[0]!='.' and os.path.isfile(file_path+file):
                files=files+file+'#'
        self.connfd.send(files.encode())

    def do_get(self,filename):
        try:
            fd=open(file_path+filename,'rb')
        except:
            self.connfd.send('文件不存在'.encode())
            return
        self.connfd.send(b'ok')
        time.sleep(.1)
        while True:
            data=fd.read(1024)
            if not data:
                time.sleep(.1)
                self.connfd.send(b'##')
                break
            self.connfd.send(data)
        print("文件发送完毕")

#创建套接字，接收客户端连接，创建新的进程
def main():
    global addr
    sockfd=socket()
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(addr)
    sockfd.listen(5)

    #处理子进程退出
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    print("listen the port 8000")

    while True:
        try:
            connfd,addr=sockfd.accept()
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit("服务器退出")
        except Exception as e:
            print("服务器异常：",e)
            continue

        print("已连接客户端",addr)

        pid=os.fork()
        if pid==0:
            sockfd.close()
            #判断客户端请求
            ftp=FtpServer(connfd)
            while True:
                data=connfd.recv(1024).decode()
                if not data or data[0]=='Q':
                    connfd.close()
                    sys.exit("客户端退出")
                elif data[0]=='L':
                    ftp.do_list()
                elif data[0]=='G':
                    filename=data.split(' ')[-1]
                    ftp.do_get(filename)

        else:
            connfd.close()
            continue


if __name__=="__main__":
    main()