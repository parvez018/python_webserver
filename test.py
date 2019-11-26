import os.path
from email.utils import formatdate

def get_file_content(file_name):
    file_cnt=""
    if(file_name=="/"):
        file_name="index.html"
    else:
        file_name=file_name[1:]
    if os.path.isfile(file_name):
        file_size = os.path.getsize(file_name)
        file_cnt = open(file_name, "r").read()
        status=200
    else:
        status=404
    return (status,file_size,file_cnt) 

def parse_req(http_req):
    req=http_req.splitlines()
    req[0]=req[0].rstrip('\r\n')
    (method,file_nm,http_version)=req[0].split()
    (status,file_size,file_content)=get_file_content(file_nm)
    headers={}
    headers["Connection:"] = "close"
    headers["Date:"] = formatdate(timeval=None, localtime=False, usegmt=True)
    headers["Server:"] = "MNASIM"
    headers["Last-Modified:"] = formatdate(timeval=None, localtime=False, usegmt=True)
    headers["Content-Length:"] = file_size
    headers["Content-Type:"] = "text/html"
    
    status_line = {}
    status_line["http_v"] = http_version
    status_line["status"] = status
    status_line["status_msg"] = "OK"
    format_response(status_line,headers,file_content)
    

def format_response(status_line,headers,data):
    response = '{http_v} {st} {st_msg}\r\n'.format(http_v=status_line["http_v"],st=status_line["status"],st_msg=status_line["status_msg"])
    for i in headers:
        # print "%s %s\r\n" % (i,headers[i])
        tmp = "%s %s\r\n" % (i,headers[i])
        response+=tmp
    response += '\r\n'
    response += data
    print response
    return response




msg="""GET /Upload/nasim.html HTTP/1.1
Host: www.google.com
Connection: close
User-agent: MNASIM
Accept-language: en""" 
# msg=msg.splitlines()
# for line in msg:
#     print line
# parse_req(msg)
file_name="index.html"
extension = os.path.splitext(file_name)[1]
print extension
n = "Upload"+file_name
print file_name[1:]
print n
import stat
st = os.stat(file_name)
print bool(st.st_mode & stat.S_IROTH)
lines = "ab cdg"
aa=lines.split()
try:
    (x,y,z)=lines.split()
    print x,y,z
except ValueError as v:
    print "error"
# info=os.stat(file_name)
# print info
# date=formatdate(timeval=info.st_mtime, localtime=False, usegmt=True)
# print date


# print msg
# req=msg.splitlines()
# print req
# print req[0]
# (method,file_nm,http_version)=req[0].split()

# print method,file_nm,http_version
# (s,f)=get_file_content(file_nm)
# print s,f
# print file
