__author__ = 'DEXTER'
import socket
address = "127.0.0.1"
port = 55555
clientSocket = socket.socket()
print "< socket created >"
clientSocket.connect((address, port))
while True:
    message = 'GetQR'
    clientSocket.send(message)
    print ">>> Sent to server"

    if message == "GetQR":
        f = open("CinemaTicket.png", "wb")
        clientSocket.settimeout(1)
        while True:
            clientRecieved = clientSocket.recv(1024)
            f.write(clientRecieved)
            f.close()
            break
        clientSocket.settimeout(None)
        print "> I recieved from server a file! "
    else:
        clientRecieved = clientSocket.recv(1024)
        print "> I recieved from server: \n", clientRecieved
        if (clientRecieved=="bye-bye") or (clientRecieved=="down"):
            clientSocket.shutdown(2)
            clientSocket.close()
            break
