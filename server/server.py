import socket
from _thread import *
File = open("info.chat","r")
g= File.read().split("\n")
ip = ""
port = int(g[1])
buff = 200
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip,port))
global humans
humans = []
def threaded_client(conn):
    try:
        while True:
            s.listen(1)
            data = conn.recv(buff)
            if data == g[0]+": close\n".encode(): 
                s.close()
                conn.close()
            print("message recieved: {",data.decode("utf-8").replace("\n",""),"}")
            for x in humans:
                x[0].send(data)  # echo
            if not data:
                conn.close()
    except:
        for x,y in enumerate(humans):
            if y[0] == conn:
                humans.pop(x)
                print("client left!, {}. note this change effects later client numbers".format(str(x)))
                for z in humans:
                    z[0].send(("user has left, CLI{}".format(str(x))).encode())
                break
while True:
    try:
        s.listen(1)
        conn,bon  =s.accept()
        if len(humans) > 1:
            if not (conn,bon) in humans:
                humans.append((conn,bon))
                start_new_thread(threaded_client,(humans[len(humans)-1][0],))
                for x in humans:
                    x[0].send(("CLI{} joined".format(str(len(humans)))).encode())
                    print(("CLI{} joined".format(str(len(humans)))))
        else:
            humans.append((conn,bon))
            start_new_thread(threaded_client,(humans[len(humans)-1][0],))
            for x in humans:
                x[0].send(("CLI{} joined".format(str(len(humans)))).encode())
                print(("CLI{} joined".format(str(len(humans)))))
    except:
        print("connection has been closed by remote host")
        break
conn.close()
