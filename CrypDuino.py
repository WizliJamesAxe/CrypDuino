from time import sleep
import sys
import serial


def discover_port():
    # if MAC get list of ports
    if sys.platform.startswith('darwin'):
        locations = glob.glob('/dev/tty.[usb*]*')
        locations = glob.glob('/dev/tty.[wchusb*]*') + locations
        locations.append('end')
    # for everyone else, here is a list of possible ports
    else:
        locations = ['dev/ttyACM0', '/dev/ttyACM0', '/dev/ttyACM1',
                     '/dev/ttyACM2', '/dev/ttyACM3', '/dev/ttyACM4',
                     '/dev/ttyACM5', '/dev/ttyUSB0', '/dev/ttyUSB1',
                     '/dev/ttyUSB2', '/dev/ttyUSB3', '/dev/ttyUSB4',
                     '/dev/ttyUSB5', '/dev/ttyUSB6', '/dev/ttyUSB7',
                     '/dev/ttyUSB8', '/dev/ttyUSB9',
                     '/dev/ttyUSB10',
                     '/dev/ttyS0', '/dev/ttyS1', '/dev/ttyS2',
                     '/dev/tty.usbserial', '/dev/tty.usbmodem', 'com2',
                     'com3', 'com4', 'com5', 'com6', 'com7', 'com8',
                     'com9', 'com10', 'com11', 'com12', 'com13',
                     'com14', 'com15', 'com16', 'com17', 'com18',
                     'com19', 'com20', 'com21', 'com1', 'end'
                     ]

    detected = None
    for device in locations:
        try:
            serial_port = serial.Serial(device, 57600, timeout=0)
            detected = device
            serial_port.close()
            break
        except serial.SerialException:
            if device == 'end':
                print('Unable to find Serial Port, Please plug in cable or check cable connections.')
                return None

    return detected


class CrypDuino:
    port = ''
    S = ''
    busy = False

    def __init__(self):
        self.port = discover_port()

    def connect_to_arduino(self):
        try:
            self.S = serial.Serial(self.port, 57600)
            return True
        except serial.SerialException:
            return False

    def send_to_arduino(self, byte_data):
        while self.busy:
            sleep(0.1)

        self.busy = True

        if len(byte_data) != 17:
            return False

        self.S.write(byte_data)
        sleep(0.1)
        result = self.S.read_all()

        self.busy = False

        return result

    def encrypt_message(self, byte_mes):
        result = ''
        while len(byte_mes) > 16:
            result += self.send_to_arduino(b'\xaa' + byte_mes[:16]).hex()
            byte_mes = byte_mes[16:]

        if len(byte_mes) != 0:
            result += self.send_to_arduino(b'\xaa' + byte_mes + b' ' * (16 - len(byte_mes))).hex()

        return result

    def decrypt_message(self, hex_mes):
        result = b''
        hex_mes = bytes.fromhex(hex_mes)

        while len(hex_mes) > 16:
            result += self.send_to_arduino(b'\xbb' + hex_mes[:16])
            hex_mes = hex_mes[16:]

        if len(hex_mes) != 0:
            result += self.send_to_arduino(b'\xbb' + hex_mes + b' ' * (16 - len(hex_mes)))

        return result.decode()


if __name__ == '__main__':
    input("Insert Arduino and press Enter.")

    arduino = CrypDuino()
    port_answer = input('Arduino inserted in ' + arduino.port + '? (YES/no)').lower()

    if port_answer == 'no':
        arduino.port = input('Specify Arduino port: ')

    while True:
        if arduino.connect_to_arduino():
            break
        else:
            print('Arduino is not inserted in ' + arduino.port + '.')
            arduino.port = input('Specify Arduino port: ')

    A = arduino.decrypt_message('5955a0b584364b3874')
    B = arduino.encrypt_message('Привет'.encode())
