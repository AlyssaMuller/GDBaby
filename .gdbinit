python  
import time
import curses
import subprocess
import sys #sys.path.insert(0, '/home/cmannett85/PrettyPrinters')

#todo add syntax linters

global myInferior
global trace_scroll #controls trace position. editable by user
trace_scroll=0
global b_list
b_list=""

def exit_curses(): #End Curses
    curses.curs_set(1) #Turn off blinking Cursor
    curses.echo() #restore echo
    curses.nocbreak() #restore needing enter after an input
    stdscr.keypad(False) #restore to no keybinding
    curses.endwin() #close app
    sys.exit(1)

def check_inferior(): #retrieve the file name from the debugging info. This will not work if the file is in another folder. Revisit if possible
    result=handle("frame") #handle('frame') command returns file and line. 
    if result:
        result=result.partition('\n')[0]
        sentence=result.split()
        where=sentence[-1]
        file_line=where.split(":")
        global trace_scroll
        global myInferior
        trace_scroll=int(file_line[1])
        myInferior=file_line[0]
        return True
    return False

def handle(cmd): #Call the appropriate gdb function
    try: 
        result=gdb.execute(cmd, to_string=True)
    except gdb.error as e:
        print("GDB call error: ", e)
        #exit_curses()
    return result 

def get_breakpoints(): #retrieve all current breakpoints
    global b_list
    b_list=handle("info breakpoints")
    b_list=b_list.split('\n')
    cleaned_list=b_list[1:]
    num_and_line=""
    #for x in cleaned_list:
        #num_and_line+=int(cleaned_list[x][0], int(cleaned_list[x][-1])
    # if result[1]=="o" #identify if it doesn't return lines of breakpoints
    #     print("no breakpoints found")
    #     return
    #print("breakpoints returns: ", num_and_line)
    return cleaned_list




def refresh_new_vars():
    #new_vars=handle("info locals")
    global local_vars
    local_vars=handle("info locals")
    #print(v_count)
    #print("var count: ", v_count)
    #print(local_vars)
    refresh_vars(local_vars)
    

def refresh_all(): #use instead of getch/individual pad refreshes to keep eveerything updating on screen at the same time
    win_update() #updates inferior code scrolling
    #print(local_vars)
    refresh_new_vars()
    #refresh_vars(local_vars, v_count)

    #code_trace.noutrefresh(trace_scroll, 0,0, int(width/2),(height-5), (width-2))  #upper-left(y,x)of pad, upper-left(y,x) of window, lower-right corner(y,x) 
    #code_trace.noutrefresh()  #upper-left(y,x)of pad, upper-left(y,x) of window, lower-right corner(y,x) aka: this onlien guide scrollY, scrollX, posY, posX, sizeY, sizeX
    #vars.noutrefresh(0,0,0,0, int(height/2), int(width/2)) #(scroll, 0, 0, 0, maxy, maxx)
    curses.doupdate() 



def refresh_vars(variables): #check if same or not and erase accordingly boo
    variables=variables.split('\n')
    for z, line in enumerate(variables[:half_height]) :
        if z==0:
            vars.addstr(0,0,"Variables:")
        vars.addnstr(z+1, 0, line, half_width-2) #add up to 2 items
        #except Exception as e:
            #print(e)
        #vars.addstr(local_vars[y])
    vars.noutrefresh() 


def win_update():
    if myInferior: #if a file is entered
        code_win.erase()
        f=open(myInferior)
        myLines=f.readlines() 
        inf_h=len(myLines)-1 #read current line instead maybe split the boys instead of read lines
        global trace_scroll
        if trace_scroll > (inf_h-height):
            trace_scroll=(inf_h-height)
            return
        if inf_h > (trace_scroll + height - 3):
            inf_h = (trace_scroll + height - 3)
        myLines=myLines[trace_scroll: inf_h]
        #print(myLines)
        for y in range(height-3):
             #bold the active line
            line_len=len(myLines[y])
            if line_len > half_width-1: #only show what's showable within the screen size
                line_len=half_width-2
            for w in range(line_len):
                #code_win.addch(y,w, myLines[y][w])
                if y>= height or w>= half_width:
                    print("inferior window out of range")
                if y==trace_scroll: #a_bold or a_standout
                    code_win.addch(y, w, myLines[y][w], curses.A_STANDOUT) #add strandout spaces for the rest of the line?
                elif isinstance(myLines[y][w], str):
                    try:
                        code_win.addch(y, w, myLines[y][w])
                    except Exception as e:
                        print("inferior code line print update error: ", e, height-1,  y, w, myLines[y][w])
        code_win.noutrefresh()

def refresh_db():
        dbInfo.addstr("Debug Info:")
        dbInfo.noutrefresh()


def break_yes(event):
    #print("reached break event yay")
    if gdb.selected_inferior().pid!=0:
        #refresh_all()
        user_ctrl()
    #print("pid=0")

def resume_me(event):
    #print("resume run!")
    user_ctrl()

#Init file stuff 
#f=input("enter a executable filename: ")
f="heap" #replace
handle("file " + str(f))
handle("start") #run and set initial breakpoint
check_inferior() #set inferior file, update scroll pos
#gdb.events.exited.connect(exit_curses) #catch any exists
#gdb.events.stop.connect(break_yes)
#gdb.events.cont.connect(resume_me)



#Init Curses
stdscr=curses.initscr() #start app
curses.start_color()
curses.noecho() # off screen input writing
curses.cbreak() #handle each keystroke without returning
stdscr.keypad(True) #key binding
curses.curs_set(0) #Turn off blinking Cursor
debug_scroll=0

#Draw Screen
height=curses.LINES
width=curses.COLS
half_width=int((width/2)-1)
half_height=int((height/2)-1)
#stdscr.addstr(1,1,"hello") #(y,x) coordinates
vars = curses.newwin(int(height/2), half_width, 0, 0) #(height, width, begin_y, begin_x)
dbInfo = curses.newwin(int(height/2), half_width, int(height/2)+1, 0) #(height, width, begin_y, begin_x)
code_win= curses.newwin(height-2, half_width-2, 0, half_width+2)
visible_cmds=curses.newwin(1, width, height-1, 0)
#local_vars=local_vars.split('\n')
#local_vars=handle("info locals")
trace_scroll=0


#visible_cmds.addstr("n:Next line b:Set Breakpoint")
#visible_cmds.noutrefresh()
stdscr.refresh() #updates screen upon launching rather than waiting for keystroke
refresh_new_vars() #grab new vars
refresh_all() #refresh all panes. 

while True:
    #print("in user control function! ")
    #global b_list
    #global trace_scroll
    if b_list!="": #looping breakpoint
        breakpoint="break"+b_list
        out=handle(breakpoint)
    c = stdscr.getch() #get raw user input commands
    if c == curses.KEY_RESIZE:
        curses.resizeterm(*stdscr.getmaxyx())
        width=curses.COLS
        height=curses.LINES
        half_width=int((width)/2)-1
        half_height=int((height)/2)-1
        stdscr.clear()
        stdscr.refresh()
    #Curses controls
    if c == curses.KEY_UP and trace_scroll>0: #scroll input code up
        trace_scroll-=1
        refresh_all()
    elif c == curses.KEY_DOWN: #scroll input code down
        trace_scroll+=1
        refresh_all() 

    ch = chr(c) #chr(ascii_val) becomes a letter
    #if ch=='r':
        #out=handle_go("run") #already in start boo
        #dbInfo.addstr(out)
        #dbInfo.noutrefresh()
        #refresh_all()
    if ch=='n': #next line
        print("next")
        try: 
            result=handle("next")
            #result=result.split()
            #result=result[0]
            #trace_scroll=int(result)
            #print("next result: " , repr(result), result)
            check_inferior()
            refresh_all()
            #trace_scroll=5
        except gdb.error as e:
            dbInfo.addstr("next command error: ", e)
            dbInfo.noutrefresh()
            print("next command exception", e)
        refresh_all()
        #print(result)
        #refresh_all()
    elif ch=='b':
        handle("clear")
        b_list=str(trace_scroll)
        breakpoint="break"+b_list
        out=handle(breakpoint)
    #elif ch=='m': #display registers

    elif ch == 'q': #113:'q' in ascii
        exit_curses()

end 

#start real gdb stuff. I am the inferior program :( The debugged)
#set startup-with-shell off #disable external shell? current error? gdb issue?
#gdb 
#handle all print
