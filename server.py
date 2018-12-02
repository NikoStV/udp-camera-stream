from definitions import *
from _thread import start_new_thread

HOST = "localhost"
HOST2 = "localhost"
#HOST = "localhost"
PORT = 8081
PORT2 = 8082
client_count = 0

#HOST = raw_input("Podaj swoj adres ip")

s1 = create_socket(HOST, PORT, 'UDP')
bind_socket(s1, HOST, PORT)
print('Starting new UDP thread')
start_new_thread(server_thread_cam, (s1, client_count))
client_count += 1
s2 = create_socket(HOST, PORT2, 'UDP')
#print(client_count)

start_new_thread(data_control_server, (s2, HOST2, PORT2))

#s2 = create_socket(HOST, PORT2, 'UDP')
#bind_socket(s2, HOST, PORT2)
#print('Starting new UDP thread')
#start_new_thread(server_thread_cam, (s2, client_count))
#client_count += 1

while True:
    pass