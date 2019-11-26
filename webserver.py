# webserver.py server_port
# The following assumptions were made

# HTTP version will always be HTTP/1.1

# Method will be always GET

# if the first line of the request does not contain 3 strings, e.g. GET /f.html HTTP/1.1

# its not considered as a well-formed request, and hence 400 error code is returned
# Upload/file.html will be accessed by link >>>>>>> host:port/file.html

# / in file name will return Upload/index.html

# for permissions, read permissions for other users group was checked only

import socket 
from thread import start_new_thread 
from email.utils import formatdate
import os.path
import stat
        
class Server:
    def __init__(self,port):
        self.port=port

    def get_file_content(self,file_name):
        file_cnt=""
        file_name=self.get_true_path(file_name)
        file_cnt = open(file_name, "r").read()
        return file_cnt 

    def get_true_path(self,file_name):
        if(file_name=="/"):
            file_name="/index.html"
        return "Upload"+file_name

    def get_file_size(self,file_name):
        file_name=self.get_true_path(file_name)
        return os.path.getsize(file_name)

    def parse_req(self,http_req):
        req=http_req.splitlines()
        req[0]=req[0].rstrip('\r\n')
        (method,file_nm,http_version)=req[0].split()
        status_line = {}
        status_line["method"] = method
        status_line["http_v"] = http_version
        return (status_line,file_nm)

    def get_content_type(self,file_name):
        ctype = {".html" : "text/html", ".jpg" : "image/jpeg", ".jpeg" : "image/jpeg", ".gif" : "image/gif" }
        file_name=self.get_true_path(file_name)
        extension = os.path.splitext(file_name)[1]
        return ctype[extension]

    def set_header(self,file_name):
        headers={}
        headers["Connection:"] = "close"
        headers["Date:"] = formatdate(timeval=None, localtime=False, usegmt=True)
        headers["Server:"] = "MNASIM"
        if(self.exist(file_name) and self.is_permission_set(file_name)):
            headers["Last-Modified:"] = formatdate(timeval=os.stat(self.get_true_path(file_name)).st_mtime, localtime=False, usegmt=True)
            headers["Content-Length:"] = self.get_file_size(file_name)
            headers["Content-Type:"] = self.get_content_type(file_name)
        return headers

    def format_response(self,status_line,headers,data):
        response = '{http_v} {st} {st_msg}\r\n'.format(http_v=status_line["http_v"],st=status_line["status"],st_msg=status_line["status_msg"])
        for i in headers:
            tmp = "%s %s\r\n" % (i,headers[i])
            response+=tmp
        response += '\r\n'
        if(status_line["status"]==200):
            response += data
        print ">>>>>>>>>>>>>>>>>>>>>>>\n",response
        return response 

    def exist(self,file_name):
        return os.path.isfile(self.get_true_path(file_name))

    def is_permission_set(self,file_name):
        file_name=self.get_true_path(file_name)
        st = os.stat(file_name)
        return bool(st.st_mode & stat.S_IROTH)
        
    def serve_request(self,connection,addr):
        try:
            msg=connection.recv(1024)
            data=""
            if(not msg):
                return
            print "Received\n",msg
            try:
                (status_line,file_name)=self.parse_req(msg)
            except ValueError as v:
                error_msg="""HTTP/1.1 400 Bad Request
Server: MNASIM
Connection: Close"""
                connection.sendall(error_msg)
                return

            # ERROR HANDLING, check if file exists, and permission set
            if(not self.exist(file_name)):
                status_line["status"]=404
                status_line["status_msg"] = "Not Found"
            elif(not self.is_permission_set(file_name)):
                status_line["status"]=403
                status_line["status_msg"] = "Permission Denied"
            else:
                status_line["status"]=200
                status_line["status_msg"] = "OK"
                data=self.get_file_content(file_name)
            
            headers=self.set_header(file_name)
            response=self.format_response(status_line,headers,data)
            connection.sendall(response)
        except socket.error as e:
            print "socket error:",repr(e)
        finally:
            connection.close() 
            print "=====" * 4, "DONE", "=====" * 4

    def start_listening(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self.sock.bind(('', self.port))
        self.sock.listen(5) 
        print "Server started at port: ",self.port
        print "=====" * 14
        while True:
            connection, adr = self.sock.accept()
            print 'Connection from ', adr[0],":",adr[1]
            start_new_thread(self.serve_request ,(connection,adr))
        self.sock.close()


if __name__ == '__main__':
    import sys
    if(len(sys.argv)!=2):
        print("python webserver.py server_port")
    else:
        s1=Server(int(sys.argv[1]))
        s1.start_listening()