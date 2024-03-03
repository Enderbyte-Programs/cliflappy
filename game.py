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

def die(stdscr):
    cursesplus.messagebox.showerror(stdscr,["You died!"])
    sys.exit()

def game(stdscr):
    lasttick = datetime.datetime.now()
    tk = 0
    stdscr.nodelay(1)
    cursesplus.displaymsg(stdscr,["Command-Line Flappy Bird"],False,False)
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
            die(stdscr)
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
        cursesplus.utils.fill_line(stdscr,0,cursesplus.set_colour(cursesplus.BLUE,cursesplus.WHITE))
        cursesplus.utils.fill_line(stdscr,stdscr.getmaxyx()[0]-1,cursesplus.set_colour(cursesplus.RED,cursesplus.WHITE))
        stdscr.addstr(0,0,f"Score: {tk//30}",cursesplus.set_colour(cursesplus.BLUE,cursesplus.WHITE))
        
        tk += 1
        if tk/60 == tk // 60:
            obstacles.append(Obstacle(tk,stdscr.getmaxyx()[0]))
        
        if tk > 500:
            stdscr.refresh()
            try:
                if chr(stdscr.inch(round(py),5)) == "█":
                    die(stdscr)
            except:
                die(stdscr)
            tosleep = (1/30*1000000 - (datetime.datetime.now()-lasttick).microseconds)/1000000
            #cursesplus.messagebox.showinfo(stdscr,[str(tosleep)])
            time.sleep(tosleep)
            stdscr.clear()
        
        lasttick = datetime.datetime.now()

curses.wrapper(game)