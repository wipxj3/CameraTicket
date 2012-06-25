__author__ = 'DEXTER'
import cv2.cv as cv
import time, socket, sys
import Image, zbar
address = 'localhost'
port = 5555
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientSocket.connect((address, port))
print '< SERVER CONNECTED >'

class CaptureImage():
    def __init__(self):
        frame = cv.CaptureFromCAM(0)
        while True:
            img = cv.QueryFrame(frame)
            cv.Rectangle(img, (140,60),(500,420), cv.RGB(0, 255, 255), 3, 8, 0)
            cv.ShowImage('QR scanner', img)
            if cv.WaitKey(10) == 27:
                break
            elif cv.WaitKey(10) == ord(' '):
                imagePath = 'D:/Dropbox/Anul III/SEM 2/APPOO/LABS/curs/qrexample/capture/'
                self.imageIndex = imagePath + self.getTime() + '_capture'
                cv.SaveImage(self.imageIndex + '.png', img)
                print '>>> Captured',self.imageIndex
                time.sleep(2)
                break
                #continue

    def getTime(self):
        t = time.localtime()
        timestamp = str(t.tm_hour)+'_'+str(t.tm_min)+'_'+str(t.tm_sec)
        return timestamp

class QRdecode():
    def __init__(self, imageIndex):
        pil = Image.open(imageIndex +'.png').convert('L')
        width, height = pil.size
        raw = pil.tostring()
        image = zbar.Image(width, height, 'Y800', raw)
        scanner = zbar.ImageScanner()
        scanner.scan(image)
        for symbol in image:
        # do something useful with results
            self.info = symbol.data
        self.data = str(self.info)

    def getData(self):
        return self.data

if __name__ == "__main__":
    while True:
        try:
            capture = CaptureImage()
            #print capture.imageIndex
            data = QRdecode(capture.imageIndex)
            #print data.getData()
            message = 'VALIDATE '
            qrData = data.getData()
            print "> Sent to server",message,'<','*'*50+qrData[48:],'>'
            clientSocket.send(message + qrData)

            if message == 'VALIDATE ':
                clientSocket.settimeout(1)
                while True:
                    clientRecieved = clientSocket.recv(1024)
                    if clientRecieved == 'VALID':
                        print '>>> VALID QRCODE'
                        raw_input('Press any key...')
                        sys.exit(0)
                    break
                clientSocket.settimeout(None)
            else:
                clientRecieved = clientSocket.recv(1024)
                print "> I recieved from server: \n", clientRecieved
                if (clientRecieved=='bye-bye') or (clientRecieved=='down'):
                    clientSocket.shutdown(2)
                    clientSocket.close()
                    break
        except Exception:
            print 'No data found!'

        if cv.WaitKey(10) == 27:
            clientSocket.shutdown(2)
            clientSocket.close()
            break
