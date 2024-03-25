import time
import curses
#import gdbcontrol, textualize, wrapper doesn't work
#from curses import wrapper

#f=input("enter a executable filename: ")

#End Curses
def exit_curses():
    curses.curs_set(1) #Turn off blinking Cursor
    curses.echo() #restore echo
    curses.nocbreak() #restore needing enter after an input
    stdscr.keypad(False) #restore to no keybinding
    curses.endwin() #close app

def refresh_scr():
    code_trace.refresh(trace_scroll, 0, 0,int(width/2), (height-5),(width-2))
    vars.getch()# upper left coordinate of pad(0,0), upper left of window to be filled(5,5), lower right corner of pad
    dbInfo.getch()

#stdscr.refresh() #updates screen to painted
#time.sleep(5)

#Init Curses
stdscr=curses.initscr() #start app
curses.start_color()
curses.noecho() # off screen input writing
curses.cbreak() #handle each keystroke without returning
stdscr.keypad(True) #key binding
curses.curs_set(0) #Turn off blinking Cursor
trace_scroll=0 #controls trace position. editable by user
debug_scroll=0

#Draw Screen
width=curses.COLS
height=curses.LINES
#stdscr.addstr(1,1,"hello") #(y,x) coordinates
vars = curses.newwin(int(height/2), int(width/2), 0, 0) #(height, width, begin_y, begin_x)
dbInfo = curses.newwin(int(height/2), int(width/2), int(height/2), 0) #(height, width, begin_y, begin_x)
for y in range(0, int(height/2)):
    for x in range(0, int(width/4)-1):
        vars.addstr('hi')

# for y in range(0, int(height/2)):
#     for x in range(0, int(width/4)):
#         dbInfo.addstr('hi')

code_trace=curses.newpad(100,100) #new pad that can show a portion of it's contents

for y in range(0, 99):
    for x in range(0, 99):
        code_trace.addch(y,x, ord('a') + (x*x+y*y) % 26)
code_trace.refresh(trace_scroll, 5, 0, int(width/2)+5, (height-5), (width-2)) # upper left coordinate of pad(0,0), upper left of window to be filled(5,5), lower right corner of pad
vars.getch()# upper left coordinate of pad(0,0), upper left of window to be filled(5,5), lower right corner of pad
dbInfo.getch()

while True:
    c = stdscr.getch() #get raw user input commands
    if c == curses.KEY_RESIZE:
        curses.resizeterm(*stdscr.getmaxyx())
        width=curses.COLS
        height=curses.LINES
        stdscr.clear()
        stdscr.refresh()
    #Curses controls
    if c == curses.KEY_UP and trace_scroll>0: #scroll input code up
        trace_scroll-=1
        code_trace.refresh(trace_scroll, 0, 0, int(width/2), (height-5), (width-2))
    elif c == curses.KEY_DOWN: #scroll input code down
        trace_scroll+=1
        code_trace.refresh(trace_scroll, 0, 0,int(width/2), (height-5),(width-2))
    elif c == 113: #'q' in ascii
        exit_curses()
        exit(1) 
        #stdscr.exit()

    ##Gdb tokenizer for commands
    # elif cmd==b:
    #     cmd='break main' #This should become the pointer location
    # elif cmd==c:
    #     cmd='continue'
    # elif cmd==d:
    #     cmd='delete main' #this should become the pointer location
    # elif cmd==i:
    #     cmd='info breakpoints' 
    # elif cmd==s:
    #     cmd="step"
    # elif cmd==r:
    #     cmd="run"
    # elif cmd==v:
    #     cmd="info locals" #local block vars? Include array of globals as well?

exit_curses()
