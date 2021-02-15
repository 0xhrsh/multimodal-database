import socket
import json
HOST = "192.168.1.69"
PORT = 8000

d = {'id': 'anand.2@iitj.ac.in', 'gender': 'm', 'age': '21', 'name': 'abc',
     'curr_city': 'xyz', 'card_used': '1580', 'fingerprint_hash': '1256'}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(json.dumps(d).encode('utf8'))
data = s.recv(1024)
print(data.decode())
s.close()
