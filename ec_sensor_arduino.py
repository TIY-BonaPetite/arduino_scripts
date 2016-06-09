# from threading import Thread
# import serial
import requests
import time

# last_received = ''
#
#
# def receiving(ser):
#     global last_received
#     buffer = ''
#     while ser.isOpen():
#         buffer = buffer + ser.read(ser.inWaiting()).decode('utf-8')
#         if '\n' in buffer:
#             lines = buffer.split('\n')  # Guaranteed to have at least 2 entries
#             last_received = lines[-2]
#             # If the Arduino sends lots of empty lines, you'll lose the
#             # last filled line, so you could make above statement conditional
#             # like so: if lines[-2]: last_received = lines[-2]
#             buffer = lines[-1]
#
#
# class SerialData(object):
#     def __init__(self, init=50):
#         try:
#             self.ser = serial.Serial(
#                 port='/dev/cu.usbmodem1421',
#                 baudrate=9600,
#                 bytesize=serial.EIGHTBITS,
#                 parity=serial.PARITY_NONE,
#                 stopbits=serial.STOPBITS_ONE,
#                 timeout=0.1,
#                 xonxoff=0,
#                 rtscts=0,
#                 interCharTimeout=None
#             )
#         except serial.serialutil.SerialException:
#             # no serial connection
#             self.ser = None
#         else:
#             thread = Thread(target=receiving, args=(self.ser,))
#             thread.daemon = True
#             thread.start()
#
#     def next(self):
#         if not self.ser:
#             return -1000  # return so we can test when Arduino isn't connected
#         # return a float value or try a few times until we get one
#         for i in range(40):
#             raw_line = last_received
#             try:
#                 return float(raw_line.strip())
#             except ValueError:
#                 # print('bogus data ', raw_line)
#                 time.sleep(.005)
#         return 0
#
#     def __del__(self):
#         if self.ser:
#             self.ser.close()


def main():
    # sleep_time = 1
    # # serial_data = SerialData()
    # time.sleep(3)
    base_url = 'http://bonapetite.herokuapp.com/'
    with requests.Session() as s:
        url = 'http://localhost:5000/login/'
        s.get(url)
        csrftoken = s.cookies['csrftoken']

        headers = {'User-Agent': 'Mozilla/5.0'}
        login_payload = {'username': 'admin',
                         'password': 'password123',
                         'csrfmiddlewaretoken': csrftoken}

        s.post(url, data=login_payload, headers=headers)

        for i in range(1):
            time.sleep(1)
            # while True:
            # time.sleep(sleep_time)
            # pH_level = serial_data.next()
            url = 'http://localhost:5000/api/mister'
            s.get(url)
            print('csrf: {}'.format(s.cookies['csrftoken']))
            csrftoken = s.cookies['csrftoken']

            sensor_payload = {'pH_level': 1111.0,
                              'temperature': 1234.0,
                              'csrfmiddlewaretoken': csrftoken}
            r = s.post('http://localhost:5000/api/mister/',
                       data=sensor_payload)
            print(r.status_code)


if __name__ == '__main__':
    main()
