import numpy as np
import socket
import sys
import cv2
import pygame
import pickle
#import Adafruit_PCA9685

class MachineControl(object):
    """"Servo Motor Control"""
    def __init__(self):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(60)

    def servcontrol(self, numb, position):
            self.pwm.set_pwm(numb, 0, position)



def create_socket(host, port, type):
    try:
        if type == 'UDP':
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        elif type == 'TCP':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            return None
        return sock
    except:
        print("Could not create socket.")
        sys.exit(0)


def bind_socket(socket, host, port):
    try:
        socket.bind((host, port))
        print("[-] Socket Bound to port " + str(port))
    except:
        print("Bind Failed")
        sys.exit(0)


def client_thread_cam(s, host, port, cap):
    while True:
        ret, frame = cap.read()
        if (ret == False):
            print('Nie wykryto kamery, zamykam watek')
            cap.release()
            s.close()
            print("[-] Socket on port " + str(port) + " closed")
            break
        else:
            cv2.imshow('frame' + str(port), frame)
            ret, buff = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 75])
            data = np.array(buff)
            stringData = data.tostring()

            count = 0
            while count < len(stringData):
                if count + 65565 > len(stringData):
                    s.sendto(stringData[count:], (host, port))
                else:
                    s.sendto(stringData[count:count + 65565], (host, port))
                count += 65565

            if cv2.waitKey(1) & 0xFF == ord('q'):
                s.close()
                cap.release()
                cv2.destroyWindow('frame' + str(port))
                print("[-] Socket on port " + str(port) + " closed")
                break


def server_thread_cam(socket, client_count):
    while True:
        img_to_read = b''
        img_to_show = b''
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyWindow('cam no ' + str(client_count))
            socket.close()
            print("Thread for camera no. " + str(client_count) + " finished")
            break

        while True:  # oczekujemy na obraz
            strng, addr = socket.recvfrom(65565)
            if len(strng) == 0:  # nie otrzymalismy wiadomosci
                if img_to_read != '':
                    img_to_show = img_to_read
                    img_to_read = ''
                break

            #if (len(strng) < 65565) and (len(strng) > 0):
                # ostatnia czesc w
            if (len(strng) < 65565) and (len(strng) > 0):
                # ostatnia czesc wiadomosci
                img_to_read += strng
                img_to_show = img_to_read
                img_to_read = ''  # obraz zapisany, wychodzimy z petli
                break

            img_to_read += strng

        img_decoded = cv2.imdecode(np.fromstring(img_to_show, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img_decoded.all != None:
            cv2.imshow('cam no ' + str(client_count), img_decoded)
        else:
            break


def data_control_server(soc, host, port):
    pygame.init()

    if pygame.joystick.get_count() != 0:

        pygame.joystick.init()
        while 1:
            event = pygame.event.get()
            joy = pygame.joystick.Joystick(0)
            joy.init()
            list = []

            for i in range(6):
                axes = joy.get_axis(i)
                list.append('{:>6.3f}'.format(axes))
            for i in range(14):
                button = joy.get_button(i)
                list.append(format(button))
                data = pickle.dumps(list)
            if data:
                soc.sendto(data, (host, port))
            else:
                break
    else:
        print('Подключите пожалуйста джостик и перезапустите программу.')

def data_control_client(soc, port):
    l=['','','','','','','','','','','','','','','','','','','','']
    #servo = MachineControl()
    while 1:
        data, server= soc.recvfrom(256)
        if data:
            inf = pickle.loads(data)
            for index, signal in enumerate(inf):
                if inf[index] != l[index]:
                    print('Команда '+str(index)+' - '+str(inf[index]))
                    l[index] = inf[index]
            data=b''
        else:
            data=b''
            break