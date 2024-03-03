import curses
import os
import sys
import random
import time
import cursesplus
import datetime
import enum

class ObstacleTypes (enum.Enum):
    Bottom = 0
    Top = 1
class Obstacle:
    def __init__(self,tick,my):
        self.otype = [ObstacleTypes.Bottom if random.randint(0,1) == 1 else ObstacleTypes.Top][0]
        self.height = random.randint(round(0.2*my),round(0.6*my))
        self.launchtick = tick

obstacles:list[Obstacle] = []

def game(stdscr):
    tk = 0
    stdscr.nodelay(1)
    py = stdscr.getmaxyx()[0]//2
    gravity = 0
    while True:
        py += gravity
        ch = stdscr.getch()
        if ch != -1 and tk > 500:
            if curses.keyname(ch) == b" " or curses.keyname(ch) == b"j":
                #cursesplus.messagebox.showinfo(stdscr,[])
                gravity = -1
        if tk > 500:
            gravity += 0.1
        try:
            stdscr.addstr(round(py),5,"P")
        except:
            print("You lose!")
            sys.exit()
        for obstacle in obstacles:
            pos = stdscr.getmaxyx()[1]-1 - round((tk - obstacle.launchtick)/5)
            if pos < 0:
                obstacles.remove(obstacle)
                continue
            if obstacle.otype == ObstacleTypes.Bottom:
                for i in range(1,obstacle.height):
                    stdscr.addstr(stdscr.getmaxyx()[0]-1-i,pos,"█")
            else:
                for i in range(0,obstacle.height):
                    stdscr.addstr(i,pos,"█") 
        
        stdscr.refresh()
        tk += 1
        if tk/60 == tk // 60:
            obstacles.append(Obstacle(tk,stdscr.getmaxyx()[0]))
        if tk > 500:
            if chr(stdscr.inch(round(py),5)) == "█":
                print("You lose!")
                sys.exit()
            time.sleep(1/30)
        stdscr.clear()

curses.wrapper(game)