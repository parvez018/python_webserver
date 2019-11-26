# webclient.py server_host server_port filename
import socket               
import sys
class Client:
    def __init__(self,host,port):
        self.host=host
        self.ip=socket.gethostbyname(host)
        self.port=int(port)
        
    def send_request(self,file_name):
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))
        msg="""/%s HTTP/1.1
Host: %s
Connection: close
User-agent: MNASIM
Accept-language: en
        """ % (file_name,self.host)
        try:
            # print self.sock.recv(1024)
            # msg=raw_input("Enter your message >>> ")
            self.sock.sendall(msg)
            response=""
            while(True):
                tmp=self.sock.recv(1024)
                if(not tmp):
                    break
                else:
                    response+=tmp    
            print "Response:\n",response
                   
        except socket.error:
            print 'Send failed'
            sys.exit()
        finally:
            self.sock.close()
    def send(self):
        # msg=raw_input("Enter your message >>> ")
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))
        msg=""
        while True:
            try:
                print self.sock.recv(1024)
                msg=raw_input("Enter your message >>> ")
                if(msg!="exit"):
                    self.sock.sendall(msg)
                else:
                    break        
            except socket.error:
                print 'Send failed'
                sys.exit()
        self.sock.close()
    def describe(self):
        print("ip:"+self.ip+" port:"+str(self.port))


if __name__ == '__main__':
    import sys
    if(len(sys.argv)!=4):
        print("python webclient.py server_host server_port filename")
    else:
        c1=Client(sys.argv[1],sys.argv[2])
        c1.send_request(sys.argv[3])