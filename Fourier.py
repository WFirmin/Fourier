import math
import numpy as np
from scipy.fft import fft, ifft
import pygame
import time


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
erase_factor = 1

to_coord = lambda pos: (pos[0]-SCREEN_WIDTH/2,-pos[1]+SCREEN_HEIGHT/2)
to_pos = lambda coord: (coord[0]+SCREEN_WIDTH/2,-coord[1]+SCREEN_HEIGHT/2)
c_to_pos = lambda c: to_pos((np.real(c),np.imag(c)))

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
running = True
drawn = False
drawing = False
X = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))
    pressed = pygame.mouse.get_pressed()[0]
    # Detect drawing phase:
    if pressed and not drawn and not drawing:
        drawn,drawing=True,True
    elif not pressed and drawing:
        drawing=False
        # Do math here:
        Y = np.array(list(map(to_coord, X[::erase_factor])))
        Y = Y[:,0]+1j*Y[:,1]
        C = fft(Y)
        T = len(Y)
        print(T)
        t = 0

    # Drawing:
    if drawing:
        pos = pygame.mouse.get_pos()
        X.append(pos)
    # Display drawing:
    if drawn:
        for i in range(len(X)-1):
            pygame.draw.line(screen, (255,255,255),X[i],X[i+1])
        if not drawing:
            pygame.draw.line(screen, (255,255,255),X[-1],X[0])
    # Display series:
    if drawn and not drawing:
        partial_sum = 0
        for i in range(len(C)):
            if np.abs(C[i])/T >= 0:
                term = C[i]*math.e**(1j*i*t)/T
                if i > 0:
                    pygame.draw.line(screen, (255,255,0),c_to_pos(partial_sum), c_to_pos(partial_sum+term))
                partial_sum += term
        pygame.draw.circle(screen, (0,0,255),list(map(int,c_to_pos(partial_sum))),3)
        t = (t + 2*math.pi/T)%(2*math.pi)
        #time.sleep(0.01)

        

    pygame.display.flip()
    time.sleep(0.005)

pygame.quit()