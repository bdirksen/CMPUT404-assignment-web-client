import socket

host = "softwareprocess.es"
port = 80
path = "/static/SoftwareProcess.es.html"

request = "GET %s HTTP/1.1\n" % path
request += "Host: %s\n" % host
request += "Accept: */*\n"
request += "Connection: close\n\n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.sendall(request.encode('utf-8'))

response = s.recv(1024).decode('utf-8')
print(response)

s.close()