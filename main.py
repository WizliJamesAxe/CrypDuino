from threading import Thread
from time import sleep
from colorama import init, Fore, Back, Style
from ApiVK import ApiVK
from CrypDuino import CrypDuino

init()


class ReadMSG(Thread):
    def __init__(self, ard, friendid, mesid):
        """Инициализация потока"""
        Thread.__init__(self)
        self.name = 'Read Message Thread'
        self.friend = friendid
        self.message_id = mesid
        self.arduino = ard

    def run(self):
        """Запуск потока"""
        while True:
            # Проверяем сообщения
            messages = user.get_unread(self.friend, self.message_id)
            for i in messages:
                try:
                    demes = self.arduino.decrypt_message(i[0])
                except:
                    continue
                self.message_id = i[1]
                while demes[-1] == ' ':
                    demes = demes[:-1]
                print(Fore.GREEN, end='')  # Change color
                print('{:>80}'.format(demes))
                print(Fore.BLUE, end='')  # Change color
            sleep(1)


class WriteMSG(Thread):
    def __init__(self, ard, friendid):
        """Инициализация потока"""
        Thread.__init__(self)
        self.name = 'Write Message Thread'
        self.friend = friendid
        self.arduino = ard

    def run(self):
        """Запуск потока"""
        while True:
            message = input().encode()
            if message == b'':
                continue
            cip_mes = self.arduino.encrypt_message(message)
            user.send_message(self.friend, cip_mes)


def start_communicate(friendid):
    print('Chat encryption is enabled!\n')
    print(Fore.BLUE, end='')  # Change color
    thread1 = WriteMSG(arduino, friendid)
    thread1.start()

    messegeid = user.send_message(friendid, 'Шифрование чата включено!')['response']
    thread2 = ReadMSG(arduino, friendid, messegeid)
    thread2.start()


if __name__ == '__main__':
    print(Back.WHITE + Fore.RED + Style.BRIGHT, end='')  # Change color
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

    try:
        file = open('settings.conf', 'r')
        configs = file.readlines()
        file.close()
    except FileExistsError:
        print('File not found!')
        exit(10)

    token = ''
    par = configs[0].split(':')
    if par[0] == 'token':
        token = par[1]
    else:
        raise BaseException('Can\'t find token in file.')

    while True:
        user = ApiVK(token)
        username = user.validate_and_get_name()
        if username is False:
            print("Token is invalid.")
            token = input('Enter correct token: ')
        else:
            print('Hello, ' + username + '!')
            break

    while True:
        try:
            idFriend = int(input('Enter friend ID: '))
            break
        except ValueError:
            print('id is a numeric string.')

    print()
    start_communicate(idFriend)
