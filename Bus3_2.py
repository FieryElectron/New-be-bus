import threading
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

#ID 1010 =>10:DE =>ZBW

global Interval
Interval = 0.5

global Command
Command = "NS 0"

def send(frame):
    for bit in frame:
        if bit == '1':
            GPIO.output(26,True)
        elif bit == '0':
            GPIO.output(26,False)
        else:
            print('Wrong Set!')
        time.sleep(Interval)
    GPIO.output(26,False)

def findtar(name):
    if name=='US':
        tar='1001'
    elif name=='DE':
        tar='1010'
    elif name=='RU':
        tar='1011'
    elif name=='CN':
        tar='1100'
    elif name=='IN':
        tar='1101'
    else:
        tar='1111'
    return tar

def findname(ID):
    if ID==9:
        name='US'
    elif ID==10:
        name='DE'
    elif ID==11:
        name='RU'
    elif ID==12:
        name='CN'
    elif ID==13:
        name='IN'
    else:
        name='XX'
    return name

def sending():
    GPIO.setup(26,GPIO.OUT)
    Star=Command[0:2]
    Snum=Command[2:]
    SBtar=findtar(Star)
    Num=int(num)
    SBnum=bin(Num).replace('0b','').zfill(8)
    SBcrc = bin(Num%9).replace('0b','').zfill(4)
    if SBtar=='1111' or Num>255:
        frame='1111000000000000'
        print('Command:',Command)
    else:
        frame=''
        frame+=SBtar
        frame+=SBnum
        frame+=SBcrc
        print('Command:',Command)
    for x in frame:
        if digit == '1':
            GPIO.output(26,True)
        elif digit == '0':
            GPIO.output(26,False)
        else:
            print('Wrong Set!')
        time.sleep(0.5)
    GPIO.output(26,False)

def recv():
    GPIO.setup(26,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    TEM=''
    while True:
        if GPIO.input(26) == True:
            time.sleep(0.01)
            for i in range(16):
                if GPIO.input(26) == True:
                    TEM += '1'
                else:
                    TEM += '0'
                time.sleep(Interval)
            #print('TEM:',TEM)
            Id = int(TEM[0:4],2)
            num = int(TEM[4:12],2)
            tar = findname(Id)
            rcrc = int(TEM[12:16],2)
            ccrc = num%9
            if rcrc==ccrc:
                Str='Verified!'
            else:
                Str='Unverified!'
            return tar,num,Str


def loop():
    tar,num,Str=recv()
    print('US => '+tar+':'+num+' '+Str)
    time.sleep(4)
    sending()
    time.sleep(2)
    tar,num,Str=recv()
    print('RU => '+tar+':'+num+' '+Str)
    time.sleep(2)

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
    def run(self):
        global Command
        while True:
            loop()
        print("Exit")

thread1 = myThread(1, "Thread-1", 1)
thread1.start()

while True:
    Command = input('')
    time.sleep(1)

print("Exit!!~~")




