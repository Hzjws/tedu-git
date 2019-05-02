from socket import *
import os,sys,time

class ftpclient():
    def __init__(self,sockfd):
        self.sockfd=sockfd

    def do_list(self):
        self.sockfd.send(b'L')
        data=self.sockfd.recv(1024).decode()
        if data=='ok':
            data=self.sockfd.recv(4096).decode()
            files=data.split('#')
            for file in files:
                print(file)
            print("查看成功")
        else:
            print(data)

    def do_get(self,filename):
        self.sockfd.send(('G '+filename).encode())
        data=self.sockfd.recv(1024).decode()
        if data=='ok':
            ft=open(filename,'wb')
            while True:
                data=self.sockfd.recv(1024)
                if data==b'##':
                    break
                ft.write(data)
            ft.close()
            print("下载完毕")
        else:
            print(data)

    def do_quit(self):
        self.sockfd.send(b'Q')
        self.sockfd.close()
        sys.exit("谢谢")
        

def main():
    if len(sys.argv)<3:
        sys.exit("err")
    host=sys.argv[1]
    port=int(sys.argv[2])
    addr=(host,port)

    sockfd=socket()
    try:
        sockfd.connect(addr)
    except:
        print("连接失败")
        return

    f=ftpclient(sockfd)
    while True:
        print("=========命令选项==========")
        print("**********list***********")
        print("*********get file********")
        print("*********put file********")
        print("**********quit***********")
        print("==========================")

        cmd=input("输入命令:")
        if cmd=='list':
            f.do_list()
        elif cmd[0]=='g':
            filename=cmd.split(' ')[-1]
            f.do_get(filename)
        elif cmd[0]=='q':
            f.do_quit()

if __name__=="__main__":
    main()