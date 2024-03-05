import time
import curses
#from curses import wrapper


#f=input("enter a executable filename: ")

#Init Curses
stdscr=curses.initscr() #start app
curses.noecho() # off screen input writing
curses.cbreak() #handle each keystroke without returning
stdscr.keypad(True) #key binding
curses.curs_set(0) #Turn off blinking Cursor



#stdscr.addstr(1,1,"hello") #(y,x) coordinates
pad=curses.newpad(100,100) #new pad that can show a portion of it's contents
# fin=open(f, "r")
# codeLen=len(fin)
# for y in range(0, codeLen%99):
#     for x in range(0, 99):
#     pad.addstr(y,x, ord('a') + (x*x+y*y) % 26)
# fin.close()

for y in range(0, 99):
    for x in range(0, 99):
        pad.addch(y,x, ord('a') + (x*x+y*y) % 26)
width=curses.COLS
height=curses.LINES
vars = curses.newwin(height, int(width/2), 0, 0) #(height, width, begin_y, begin_x)

pad_scroll=0
pad.refresh(pad_scroll,0,0,int(width/2),(height-5),(width-2)) # upper left coordinate of pad(0,0), upper left of window to be filled(5,5), lower right corner of pad
vars.refresh()# upper left coordinate of pad(0,0), upper left of window to be filled(5,5), lower right corner of pad

#stdscr.refresh() #updates screen to painted
time.sleep(5)



while True:
    c = stdscr.getch() #get user input command

    if c == curses.KEY_UP and pad_scroll>0: #scroll input code up
        pad_scroll-=1
        pad.refresh(pad_scroll,0,0,int(width/2),(height-5),(width-2))
    elif c == curses.KEY_DOWN: #scroll input code down
        pad_scroll+=1
        pad.refresh(pad_scroll,0,0,int(width/2),(height-5),(width-2))
    elif c == 113: #'q' in ascii
        curses.curs_set(1) #Turn off blinking Cursor
        curses.echo() #restore echo
        curses.nocbreak() #restore needing enter after an input
        stdscr.keypad(False) #restore to no keybinding
        curses.endwin() #close app
        #stdscr.exit()

#End Curses
curses.curs_set(1) #Turn off blinking Cursor
curses.echo() #restore echo
curses.nocbreak() #restore needing enter after an input
stdscr.keypad(False) #restore to no keybinding

curses.endwin() #close app

