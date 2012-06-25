__author__ = 'DEXTER'
import socket, time
address = "localhost"
port = 5555
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((address, port))
print "< SERVER CONNECTED >"
while True:
    message = 'generate '
    criteria = ['cinema', 'day', 'time_stamp', 'movie', 'locul']
    lst = [int(raw_input('Input '+str(criteria[i])+': ')) for i in range(0,5)]
    request = str(lst[0])+','+ str(lst[1]) +','+ str(lst[2]) +','+ str(lst[3]) +','+ str(lst[4])
    print request
    clientSocket.send(message + request)

    if message[:9] == 'generate ':
        f = open('./phone/CinemaTicket.png', 'wb')
        while True:
            buf = clientSocket.recv(4096)
            f.write(buf)
            f.close()
            break
        print "> I recieved from server a file! "

        break
    else:
        clientRecieved = clientSocket.recv(4096)
        print "> I recieved from server: \n", clientRecieved
        if (clientRecieved=="bye-bye") or (clientRecieved=="down"):
            clientSocket.shutdown(2)
            clientSocket.close()
            break
