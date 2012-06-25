__author__ = 'DEXTER'
import hashlib, base64
import os, sqlite3, time
import qrcode, places

class QRencode():
    def __init__(self):
        criteria = ['cinema', 'day', 'time_stamp', 'movie', 'locul']
        lst = [int(raw_input('Input '+str(criteria[i])+': ')) for i in range(0,5)]

        self.salt = str(os.urandom(128))
        self.info = places.cinema[int(lst[0])] +'_'\
               + places.day[int(lst[1])] +'_'\
               + places.time_stamp[int(lst[2])] +'_'\
               + places.movie[int(lst[3])] +'_'\
               + places.locul[int(lst[4])]
        self.data = base64.b64encode(hashlib.sha512(self.salt + self.info).hexdigest())

    def getTime(self):
        t = time.localtime()
        timestamp = str(t.tm_hour)+'_'+str(t.tm_min)+'_'+str(t.tm_sec)
        return timestamp

    def getData(self):
        return [self.info, self.data[30:84]]

    def generate(self, data):
        qr = qrcode.QRCode(
            version=5,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=3,
        )
        qr.add_data(data)
        qr.make(fit=True)
        im = qr.make_image()
        timestamp = self.getTime()
        imageIndex = timestamp + '_qr'
        im.save(imageIndex + '.png')
        return imageIndex

    def saveToDB(self, qrImage, info, qrHash):
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        # Insert a row of data
        c.execute("INSERT INTO QRs VALUES (?, ?, ? ,?)", (None ,qrImage, info, qrHash))
        # Save (commit) the changes
        conn.commit()
        # We can also close the cursor if we are done with it
        c.close()
        return 'added to DB!'

    def verifyHash(self, recvHash):
        con = sqlite3.connect('test.db')
        with con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM QRs WHERE qrHash=?", (recvHash,))
            rows = cur.fetchall()
            if len(rows) == 1:
                response = 'valid'
            else:
                print rows
                response = 'invalid'
            return response

if __name__ == "__main__":
    qr = QRencode()
    info, qrHash = qr.getData()
    qrImage = qr.generate(qrHash)
    print info
    print qrHash
    print qrImage
    qr.saveToDB(str(qrImage), str(info), str(qrHash))
    rvHash = 'ZkNmM1NTRkNDQ2NjYyNTA1NGE5YzQ3MmNmZDY2ZTBmNzBhNGVlMzYw'
    check = qr.verifyHash(rvHash)
    print check
    print 'DONE!'


