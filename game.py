#!/usr/bin/python3

import curses
import os
import sys
import random
import time
import cursesplus
import datetime
import signal
import enum

INGAME = False
SCREEN = None

HELP = """
How To Play

Press the space bar to move up

Don't hit the obstacles
Don't fall off the bottom
Don't go too high

For if you do, you will DIE!

Have fun...
"""

def help(stdscr):
    cursesplus.textview(stdscr,text=HELP)

def ctrlchandler(sig,frame):
    if INGAME:
        SCREEN.nodelay(0)
    msg = ["Are you sure you wish to quit?"]
    if INGAME:
        msg.append("You will lose your progress in this game.")
    if cursesplus.messagebox.askyesno(SCREEN,msg):
        sys.exit()
    if INGAME:
        SCREEN.nodelay(1)

def menu(stdscr):
    signal.signal(signal.SIGINT,ctrlchandler)

    global SCREEN
    global INGAME
    SCREEN = stdscr
    cursesplus.utils.hidecursor()

    while True:
        wtd = cursesplus.coloured_option_menu(stdscr,["Play Game!","Settings","Statistics","Help","Quit"],"Command Line Flappy Bird! Choose an option.",[["quit",cursesplus.RED],["play",cursesplus.GREEN],["help",cursesplus.CYAN]])
        if wtd == 0:
            stdscr.nodelay(1)
            recentscore = game(stdscr)
            INGAME = False
            stdscr.nodelay(0)#Back to char only
        elif wtd == 3:
            help(stdscr)
        elif wtd == 4:
            break
    cursesplus.utils.showcursor()

class ObstacleTypes (enum.Enum):
    Bottom = 0
    Top = 1
class Obstacle:
    def __init__(self,tick,my,score=0):
        my += 1#Compensate for bottom
        self.otype = [ObstacleTypes.Bottom if random.randint(0,1) == 1 else ObstacleTypes.Top][0]
        maximium = 0.6
        if score > 100:
            maximium = 0.7
        self.height = random.randint(round(0.3*my),round(maximium*my))
        self.launchtick = tick

def game(stdscr) -> int:
    global INGAME
    INGAME = True
    obstacles:list[Obstacle] = []
    BOTTOM = stdscr.getmaxyx()[0]-1
    #15 Ys between obstacles
    #((mx*2)-2)*30
    sleepyTick = ((stdscr.getmaxyx()[1]*2)-2*15)
    lasttick = datetime.datetime.now()
    tk = 0
   
    cursesplus.displaymsg(stdscr,["Command-Line Flappy Bird"],False,False)
    py = BOTTOM//2
    gravity = 0
    while True:
        py += gravity
        
        ch = stdscr.getch()
        if ch != -1 and tk > sleepyTick:
            if curses.keyname(ch) == b" " or curses.keyname(ch) == b"j":
                #cursesplus.messagebox.showinfo(stdscr,[])
                gravity = -1
        if tk > sleepyTick:
            gravity += 0.1
        try:
            stdscr.addstr(round(py),5,"P")
        except:
            cursesplus.messagebox.showerror(stdscr,["You died!"])
            return (tk-sleepyTick)//30
        for obstacle in obstacles:
            pos = stdscr.getmaxyx()[1]-1 - round((tk - obstacle.launchtick)//2)
            if pos < 0:
                obstacles.remove(obstacle)
                continue
            if obstacle.otype == ObstacleTypes.Bottom:
                for i in range(1,obstacle.height):
                    stdscr.addstr(BOTTOM-i,pos,"█")
            else:
                for i in range(0,obstacle.height):
                    stdscr.addstr(i,pos,"█") 
        cursesplus.utils.fill_line(stdscr,0,cursesplus.set_colour(cursesplus.BLUE,cursesplus.WHITE))
        cursesplus.utils.fill_line(stdscr,BOTTOM,cursesplus.set_colour(cursesplus.RED,cursesplus.WHITE))
        stdscr.addstr(0,0,f"Score: {(tk-sleepyTick)//30}",cursesplus.set_colour(cursesplus.BLUE,cursesplus.WHITE))
        
        tk += 1
        if tk/30 == tk // 30:
            obstacles.append(Obstacle(tk,BOTTOM,(tk-sleepyTick)//30))
        
        if tk > sleepyTick:
            stdscr.refresh()
            try:
                if chr(stdscr.inch(round(py),5)) == "█":
                    cursesplus.messagebox.showerror(stdscr,["You died!"])
                    return (tk-sleepyTick)//30
            except:
                cursesplus.messagebox.showerror(stdscr,["You died!"])
                return (tk-sleepyTick)//30
            tosleep = (1/30*1000000 - (datetime.datetime.now()-lasttick).microseconds)/1000000
            if tosleep > 0:#Prevent crash in laggy confitions
                time.sleep(tosleep)
            stdscr.clear()
        
        lasttick = datetime.datetime.now()

curses.wrapper(menu)