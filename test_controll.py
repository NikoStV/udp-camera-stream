import pygame
import pickle

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
        byt = pickle.dumps(list)
        load = pickle.loads(byt)
        print(load)
else:
    print('Подключите пожалуйста джостик и перезапустите программу.')