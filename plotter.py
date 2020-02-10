from time import sleep

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import serial

s = serial.Serial()
s.port = "COM3"
s.baudrate = 115200
s.timeout = 10
s.open()
if s.isOpen:
    print("Serial port open")

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
t = []
pos_cmd = []
pos_act = []

s.write(b"\n")

t_start = int(s.readline().split(b",")[0])

def animate(i, xs, ys):
    line=s.readline()
    line = line.split(b',')
    try:
        t.append(int(line[0]) - t_start)
        pos_cmd.append(float(line[1]))
        pos_act.append(float(line[2]))
    except ValueError:
        pass
    
    ax.clear()
    ax.plot(t, pos_cmd, label="Commanded Position")
    ax.plot(t, pos_act, label="Actual Position")
    
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Motor Response')
    plt.ylabel('Position (%)')
    plt.xlabel('Time (ms)')
    plt.legend()
    plt.axis([1, None, -100, 100]) #Use for arbitrary number of trials
    #plt.axis([1, 100, 0, 1.1]) #Use for 100 trial demo
    
    plt.pause(0.001)
    
    
ani = animation.FuncAnimation(fig, animate, fargs=(pos_cmd, pos_act), interval=1)
plt.show(block=False)
while True:
    pos = input("enter target position")
    if ("q" == pos): exit()
    s.write(b"r\n")
    sleep(0.5)
    s.write(pos.encode('ascii'))
    s.write(b"\n")
plt.show()
