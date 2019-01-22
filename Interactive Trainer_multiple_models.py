
# coding: utf-8

# In[1]:


import pygame, sys
from pygame.locals import *
import numpy as np
import socket
import ast
#import subprocess
import serial


UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 8888
Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Sock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))


# In[2]:


#### This is for training


# In[3]:


def draw_target(direction): # 0,0 is the top left of the rect
    
    #global top_count, right_count, bottom_count, left_count
    global overall_count
   
    if direction == 'Top':
        dir = 0
        pygame.draw.rect(DISPLAYSURF, RED, (0, 0, wd, 4)) #top
    elif direction == 'Left':
        dir = 1
        pygame.draw.rect(DISPLAYSURF, RED, (0, 0, 4, ht)) #left
    elif direction == 'Bottom':
        dir = 2
        pygame.draw.rect(DISPLAYSURF, RED, (0, ht-4, wd, 4)) # bottom
    elif direction == 'Right':
        dir = 3
        pygame.draw.rect(DISPLAYSURF, RED, (wd-4, 0, 4, ht)) #right
    
    overall_count +=1
    return dir


# In[4]:


##### This is for testing


# In[5]:


def draw_random_target(): # 0,0 is the top left of the rect
    
    #global top_count, right_count, bottom_count, left_count
    global test_count
    dir = np.random.choice(4)
   
    if dir == 0:
        pygame.draw.rect(DISPLAYSURF, RED, (0, 0, wd, 4)) #top
    elif dir == 1:
        pygame.draw.rect(DISPLAYSURF, RED, (0, 0, 4, ht)) #left
    elif dir == 2:
        pygame.draw.rect(DISPLAYSURF, RED, (0, ht-4, wd, 4)) # bottom
    elif dir == 3:
        pygame.draw.rect(DISPLAYSURF, RED, (wd-4, 0, 4, ht)) #right
    
    test_count +=1
    return dir


# In[6]:


from keras.models import Sequential
from keras.layers import Dense, Activation

model1 = Sequential([
    Dense(4, input_shape=(8,)),
    Activation('relu'),
    Dense(2),
    Activation('linear'),
])

model1.compile(optimizer='rmsprop', loss='mse')

model2 = Sequential([
    Dense(4, input_shape=(8,)),
    Activation('relu'),
    Dense(2),
    Activation('linear'),
])

model2.compile(optimizer='rmsprop', loss='mse')

model3 = Sequential([
    Dense(4, input_shape=(8,)),
    Activation('relu'),
    Dense(2),
    Activation('linear'),
])

model3.compile(optimizer='rmsprop', loss='mse')

model4 = Sequential([
    Dense(4, input_shape=(8,)),
    Activation('relu'),
    Dense(2),
    Activation('linear'),
])

model4.compile(optimizer='rmsprop', loss='mse')


# In[7]:


###### model for top


# In[8]:


# activate OpenBCI
# cd /Downloads/OpenBCI...
# python user.py -p COM4 --add udp_server

pygame.init()

FPS = 50
fpsClock = pygame.time.Clock()

ht = 400
wd = 400
DISPLAYSURF = pygame.display.set_mode((wd, ht),0,32)
pygame.display.set_caption('Hello World!')

BLACK =(0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)


DISPLAYSURF.fill(WHITE)

overall_count = 1
tar_dir = draw_target('Top') #0=Up, 1=Left, 2=Down, 3=Right


ball_x = int(wd/2)
ball_y = int(ht/2)

nn_in = []
nn_out = []

#mv = np.random.rand(1)
#mh = np.random.rand(1)
while overall_count < 21: # main game loop
            
    pygame.draw.circle(DISPLAYSURF, BLUE, (ball_x, ball_y), 5, 0)
    
    # take input signals here
    mag_in, addr = Sock.recvfrom(1024)
    ###Getting the eeg signals and performing some data processing on that
    mag_in = np.asarray(ast.literal_eval(mag_in.decode("utf-8"))).reshape(1,8)
    mag_in = np.nan_to_num(mag_in)/max(abs(np.nan_to_num(mag_in)))
    
    #mag_in = np.random.rand(8).reshape(1,8)
    ###the eeg signal is fed as input to the model
    mov_out = model1.predict(mag_in)
    
    mv = mov_out[0,1]
    mh = mov_out[0,0]
  
    ### Getting the location of the red line in the square and assigning act_dir with the appropriate direction

    act_dir = [0,-1]
    
    nn_in.append(mag_in)
    nn_out.append(act_dir)
    ball_x += int(5*mh)
    ball_y += int(5*mv)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if ball_x<=5 or ball_x>=wd-5 or ball_y<=5 or ball_y>=ht-5:
        #print(dir)
        if overall_count%10==0 :
            data = (np.asarray(nn_in))
            data = data.reshape(int(data.size/8),8)
            labels = np.asarray(nn_out)
            print(mov_out)
            print(act_dir)
            model1.fit(data, labels, epochs=1, batch_size=2)
            nn_in = []
            nn_out = []

        DISPLAYSURF.fill(WHITE)
        tar_dir = draw_target('Top')
        ball_x = int(wd/2)
        ball_y = int(ht/2)
        #QUIT
            
    pygame.display.update()
    fpsClock.tick(FPS)


# In[9]:


##### model for right


# In[10]:


# activate OpenBCI
# cd /Downloads/OpenBCI...
# python user.py -p COM4 --add udp_server

pygame.init()

FPS = 50
fpsClock = pygame.time.Clock()

ht = 400
wd = 400
DISPLAYSURF = pygame.display.set_mode((wd, ht),0,32)
pygame.display.set_caption('Hello World!')

BLACK =(0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)


DISPLAYSURF.fill(WHITE)
dir = -1
overall_count = 1
tar_dir = draw_target('Right') #0=Up, 1=Left, 2=Down, 3=Right
success = 0

ball_x = int(wd/2)
ball_y = int(ht/2)

nn_in = []
nn_out = []

#mv = np.random.rand(1)
#mh = np.random.rand(1)
while overall_count < 21: # main game loop
            
    pygame.draw.circle(DISPLAYSURF, BLUE, (ball_x, ball_y), 5, 0)
    
    # take input signals here
    mag_in, addr = Sock.recvfrom(1024)
    ###Getting the eeg signals and performing some data processing on that
    mag_in = np.asarray(ast.literal_eval(mag_in.decode("utf-8"))).reshape(1,8)
    mag_in = np.nan_to_num(mag_in)/max(abs(np.nan_to_num(mag_in)))
   
    #mag_in = np.random.rand(8).reshape(1,8)
    ###the eeg signal is fed as input to the model
    mov_out = model2.predict(mag_in)
    
    mv = mov_out[0,1]
    mh = mov_out[0,0]
    
    
    ### Getting the location of the red line in the square and assigning act_dir with the appropriate direction
    act_dir = [1,0]


    nn_in.append(mag_in)
    nn_out.append(act_dir)
    ball_x += int(5*mh)
    ball_y += int(5*mv)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
   
    if ball_x<=5 or ball_x>=wd-5 or ball_y<=5 or ball_y>=ht-5:
        #print(dir)
        if overall_count%10==0 :
            data = (np.asarray(nn_in))
            data = data.reshape(int(data.size/8),8)
            labels = np.asarray(nn_out)

            model2.fit(data, labels, epochs=1, batch_size=2)
            nn_in = []
            nn_out = []

        DISPLAYSURF.fill(WHITE)
        tar_dir = draw_target('Right')
        ball_x = int(wd/2)
        ball_y = int(ht/2)
        #QUIT
            
    pygame.display.update()
    fpsClock.tick(FPS)


# In[11]:


##### model for bottom


# In[12]:


# activate OpenBCI
# cd /Downloads/OpenBCI...
# python user.py -p COM4 --add udp_server

pygame.init()

FPS = 50
fpsClock = pygame.time.Clock()

ht = 400
wd = 400
DISPLAYSURF = pygame.display.set_mode((wd, ht),0,32)
pygame.display.set_caption('Hello World!')

BLACK =(0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)


DISPLAYSURF.fill(WHITE)

overall_count = 1
tar_dir = draw_target('Bottom') #0=Up, 1=Left, 2=Down, 3=Right
success = 0

ball_x = int(wd/2)
ball_y = int(ht/2)

nn_in = []
nn_out = []

#mv = np.random.rand(1)
#mh = np.random.rand(1)
while overall_count < 21: # main game loop
            
    pygame.draw.circle(DISPLAYSURF, BLUE, (ball_x, ball_y), 5, 0)
    
    # take input signals here
    mag_in, addr = Sock.recvfrom(1024)
    ###Getting the eeg signals and performing some data processing on that
    mag_in = np.asarray(ast.literal_eval(mag_in.decode("utf-8"))).reshape(1,8)
    mag_in = np.nan_to_num(mag_in)/max(abs(np.nan_to_num(mag_in)))
   
    #mag_in = np.random.rand(8).reshape(1,8)
    ###the eeg signal is fed as input to the model
    mov_out = model3.predict(mag_in)
    
    mv = mov_out[0,1]
    mh = mov_out[0,0]
    
    
    ### Getting the location of the red line in the square and assigning act_dir with the appropriate direction
    act_dir = [0,1]


    nn_in.append(mag_in)
    nn_out.append(act_dir)
    ball_x += int(5*mh)
    ball_y += int(5*mv)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
   
    if ball_x<=5 or ball_x>=wd-5 or ball_y<=5 or ball_y>=ht-5:
        #print(dir)
        if overall_count%10==0 :
            data = (np.asarray(nn_in))
            data = data.reshape(int(data.size/8),8)
            labels = np.asarray(nn_out)

            model3.fit(data, labels, epochs=1, batch_size=2)
            nn_in = []
            nn_out = []


        DISPLAYSURF.fill(WHITE)
        tar_dir = draw_target('Bottom')
        ball_x = int(wd/2)
        ball_y = int(ht/2)
        #QUIT
            
    pygame.display.update()
    fpsClock.tick(FPS)


# In[13]:


##### model for left


# In[14]:


# activate OpenBCI
# cd /Downloads/OpenBCI...
# python user.py -p COM4 --add udp_server

pygame.init()

FPS = 50
fpsClock = pygame.time.Clock()

ht = 400
wd = 400
DISPLAYSURF = pygame.display.set_mode((wd, ht),0,32)
pygame.display.set_caption('Hello World!')

BLACK =(0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)


DISPLAYSURF.fill(WHITE)

overall_count = 1
tar_dir = draw_target('Left') #0=Up, 1=Left, 2=Down, 3=Right
success = 0

ball_x = int(wd/2)
ball_y = int(ht/2)

nn_in = []
nn_out = []

mv = np.random.rand(1)
mh = np.random.rand(1)
while overall_count < 21: # main game loop
            
    pygame.draw.circle(DISPLAYSURF, BLUE, (ball_x, ball_y), 5, 0)
    
    # take input signals here
    mag_in, addr = Sock.recvfrom(1024)
    ###Getting the eeg signals and performing some data processing on that
    mag_in = np.asarray(ast.literal_eval(mag_in.decode("utf-8"))).reshape(1,8)
    mag_in = np.nan_to_num(mag_in)/max(abs(np.nan_to_num(mag_in)))
   
    #mag_in = np.random.rand(8).reshape(1,8)
    ###the eeg signal is fed as input to the model
    mov_out = model4.predict(mag_in)
    
    mv = mov_out[0,1]
    mh = mov_out[0,0]
    
    
    ### Getting the location of the red line in the square and assigning act_dir with the appropriate direction
    act_dir = [-1,0]


    nn_in.append(mag_in)
    nn_out.append(act_dir)
    ball_x += int(5*mh)
    ball_y += int(5*mv)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
   
    if ball_x<=5 or ball_x>=wd-5 or ball_y<=5 or ball_y>=ht-5:
        #print(dir)
        if overall_count%10==0 :
            data = (np.asarray(nn_in))
            data = data.reshape(int(data.size/8),8)
            labels = np.asarray(nn_out)

            model4.fit(data, labels, epochs=1, batch_size=2)
            nn_in = []
            nn_out = []

        DISPLAYSURF.fill(WHITE)
        tar_dir = draw_target('Left')
        ball_x = int(wd/2)
        ball_y = int(ht/2)
        #QUIT
            
    pygame.display.update()
    fpsClock.tick(FPS)


# In[15]:


#### testing


# This will not yield proper output with the random generator. With the EEG, the assumption is the signals corresponding to TRBL are distinct and when a new signal is given, the model which has seen that kind of/ similar input will give an output closest to its label. And then am assigning that model for the remaining movement of the ball. I guess logic wise it is fine - but whether there will be difference in the signals is a moot point.

# In[19]:


#inintialize arm
ser = serial.Serial()
ser.port = 'COM4'
ser.open()
ser.write(b'm')


# In[20]:


# activate OpenBCI
# cd /Downloads/OpenBCI...
# python user.py -p COM4 --add udp_server

pygame.init()

FPS = 50
fpsClock = pygame.time.Clock()

ht = 400
wd = 400
DISPLAYSURF = pygame.display.set_mode((wd, ht),0,32)
pygame.display.set_caption('Hello World!')

BLACK =(0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)


DISPLAYSURF.fill(WHITE)

test_count = 1
tar_dir = draw_random_target() #0=Up, 1=Left, 2=Down, 3=Right
success = 0

top_dir = [0,-1]
right_dir = [1,0]
bottom_dir = [0,1]
left_dir = [-1,0]


ball_x = int(wd/2)
ball_y = int(ht/2)

nn_in = []
nn_out = []

#mv = np.random.rand(1)
#mh = np.random.rand(1)
#initialize
#ser.write(b'm')
flag = 0
while test_count < 10: # main game loop
    #print("in main loop")
    
            
    pygame.draw.circle(DISPLAYSURF, BLUE, (ball_x, ball_y), 5, 0)
    
    # take input signals here
    mag_in, addr = Sock.recvfrom(1024)
    ###Getting the eeg signals and performing some data processing on that
    mag_in = np.asarray(ast.literal_eval(mag_in.decode("utf-8"))).reshape(1,8)
    mag_in = np.nan_to_num(mag_in)/max(abs(np.nan_to_num(mag_in)))
   
    #mag_in = np.random.rand(8).reshape(1,8)
    ###the eeg signal is fed as input to the model
    mov_out_1 = (model1.predict(mag_in)[0,0]-top_dir[0])**2 + (model1.predict(mag_in)[0,1]-top_dir[1])**2
    mov_out_2 = (model2.predict(mag_in)[0,0]-right_dir[0])**2 + (model2.predict(mag_in)[0,1]-right_dir[1])**2
    mov_out_3 = (model3.predict(mag_in)[0,0]-bottom_dir[0])**2 + (model3.predict(mag_in)[0,1]-bottom_dir[1])**2
    mov_out_4 = (model4.predict(mag_in)[0,0]-left_dir[0])**2 + (model4.predict(mag_in)[0,1]-left_dir[1])**2
    
    if min(mov_out_1, mov_out_2, mov_out_3, mov_out_4)==mov_out_1: #Topmv mv<0 go up 
        ser.write(b'a')
        print('top')
        mov_out = model1.predict(mag_in)
        
    elif min(mov_out_1, mov_out_2, mov_out_3, mov_out_4)==mov_out_2: #Right mh<0 left
        ser.write(b'e')
        print('right')
        mov_out = model2.predict(mag_in)
        
    elif min(mov_out_1, mov_out_2, mov_out_3, mov_out_4)==mov_out_3: #Bottom
        ser.write(b'z')
        print('bottom')
        mov_out = model3.predict(mag_in)
        
    else: #Left
        ser.write(b'q')
        print('left')
        mov_out = model4.predict(mag_in)
        
    print(mov_out)
    
    
    mv = mov_out[0,1]
    mh = mov_out[0,0]
    
    #print(mov_out_1,mov_out_2, mov_out_3, mov_out_4)
    ### Getting the location of the red line in the square and assigning act_dir with the appropriate direction
    #act_dir = [-1,0]


    #nn_in.append(mag_in)
    #nn_out.append(act_dir)
    ball_x += int(2*mh)
    ball_y += int(2*mv)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
   
    if ball_x<=5 or ball_x>=wd-5 or ball_y<=5 or ball_y>=ht-5:
        DISPLAYSURF.fill(WHITE)
        tar_dir = draw_random_target()
        ball_x = int(wd/2)
        ball_y = int(ht/2)
        #print(dir)
       # if overall_count%10==0 :
        #    data = (np.asarray(nn_in))
         #   data = data.reshape(int(data.size/8),8)
          #  labels = np.asarray(nn_out)

           # model4.fit(data, labels, epochs=1, batch_size=2)
           # nn_in = []
           # nn_out = []

        
            
    pygame.display.update()
    fpsClock.tick(FPS)


# In[18]:


ser.write(b'm')
Sock.close()
ser.close()

