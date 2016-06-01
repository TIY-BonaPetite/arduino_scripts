from threading import Thread
import time
import serial

last_received = ''


def receiving(ser):
    global last_received
    buffer = ''
    while True:
        buffer = buffer + ser.read(ser.inWaiting())
        if '\n' in buffer:
            lines = buffer.split('\n')  # Guaranteed to have at least 2 entries
            last_received = lines[-2]
            # If the Arduino sends lots of empty lines, you'll lose the
            # last filled line, so you could make above statement conditional
            # like so: if lines[-2]: last_received = lines[-2]
            buffer = lines[-1]


class SerialData(object):
    def __init__(self, init=50):
        try:
            self.ser = serial.Serial(
                port='/dev/cu.usbmodem1421',
                baudrate=9600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=0.1,
                xonxoff=0,
                rtscts=0,
                interCharTimeout=None
            )
        except serial.serialutil.SerialException:
            # no serial connection
            self.ser = None
        else:
            self.thread = Thread(target=receiving, args=(self.ser,))
            self.thread.start()

    def next(self):
        if not self.ser:
            return -1000  # return so we can test when Arduino isn't connected
        # return a float value or try a few times until we get one
        for i in range(40):
            raw_line = last_received
            try:
                return float(raw_line.strip())
            except ValueError:
                print('bogus data ', raw_line)
                time.sleep(.005)
        return 0.

    def __del__(self):
        if self.ser:
            self.ser.close()

if __name__ == '__main__':
    s = SerialData()
    for i in range(10):
        time.sleep(.015)
        print(s.next())
    # print('foo')
    # s.thread._Thread__stop()
    # print('bar')
