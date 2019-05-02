from socket import *
import sys,time

#基本文件操作功能
class FtpClient(object):
    def __init__(self,sockfd):
        self.sockfd=sockfd

    def do_list(self):
        self.sockfd.send(b'L')
        #等待回复
        data=self.sockfd.recv(1024).decode()
        if data=='ok':
            data=self.sockfd.recv(4096).decode()
            files=data.split('#')
            for file in files:
                print(file)
            print("文件列表展示完毕")
        else:
            print(data)

    def do_get(self,filename):
        self.sockfd.send(('G '+filename).encode())
        data=self.sockfd.recv(1024).decode()
        if data=='ok':
            fd=open(filename,'wb')
            while True:
                data=self.sockfd.recv(1024)
                if data==b'##':
                    break
                fd.write(data)
            fd.close()
            print("下载完毕")
        else:
            print(data)

    def do_quit(self):
        self.socket.send(b'Q')


#网络连接
def main():
    if len(sys.argv)<3:
        print("argv is err")
        return
    host=sys.argv[1]
    port=int(sys.argv[2])
    addr=(host,port)

    sockfd=socket()
    try:
        sockfd.connect(addr)
    except:
        print("连接服务器失败")
        return

    ftp=FtpClient(sockfd)

    while True:
        print("=========命令选项==========")
        print("**********list***********")
        print("*********get file********")
        print("*********put file********")
        print("**********quit***********")
        print("==========================")

        cmd=input("请输入命令：")

        if cmd.strip()=='list':
            ftp.do_list()
        elif cmd[:3]=='get':
            filename=cmd.split(' ')[-1]
            ftp.do_get(filename)
        elif cmd.strip()=='quit':
            ftp.do_quit()
            sockfd.close()
            sys.exit("谢谢使用")
        else:
            print("请正确输入")
            continue




if __name__=="__main__":
    main()