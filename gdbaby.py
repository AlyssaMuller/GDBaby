#!/usr/bin/env python3
from pygdbmi.gdbcontroller import GdbController
import curses
import time
import sys 

gdbmi = GdbController()
#gdbmi.write('-file-exec-and-symbols a.out')
#gdbmi.write('break main') # machine interface (MI) commands start with a '-'
#response = gdbmi.write('-exec-run --start')


#todo add syntax linters

global myInferior
global trace_scroll #controls trace position. editable by user
trace_scroll=0
global b_list
b_list=""
global var_list

def exit_curses(): #End Curses
    curses.curs_set(1) #Turn off blinking Cursor
    curses.echo() #restore echo
    curses.nocbreak() #restore needing enter after an input
    stdscr.keypad(False) #restore to no keybinding
    curses.endwin() #close app
    sys.exit(1)

def continue_inf():
    result=handle("frame")
    print(result)

def check_inferior(): #retrieve the file name from the debugging info. This will not work if the file is in another folder. Revisit if possible
    result=handle("frame") #handle('frame') command returns file and line.
    #print("reached check inferior: ", result)
    for i in result:
        if i["message"]=="i/o":
            result=result["payload"]["frame"]
            global trace_scroll
            global myInferior
            myInferior=str(result["fullname"])
            trace_scroll=int(result["line"])

    #result=result.split()
    #result=result[-1]
    #print(result)
    #result=result.split(":")
    #global trace_scroll
    #global myInferior
    #print(result)
    #time.sleep(5)
    #trace_scroll=int(result[1])
    #myInferior='practice.c'  #result[0]
    return

def handle(cmd): #Call the appropriate gdb function
    result=gdbmi.write(cmd)
    return result 

def get_breakpoints(): #retrieve all current breakpoints defunct only doing one at a time
    global b_list
    b_list=handle("info breakpoints")
    #b_list=b_list.split('\n')
    cleaned_list=b_list[1:]
    print(cleaned_list)
    time.sleep(5)
    num_and_line=""
    #for x in cleaned_list:
        #num_and_line+=int(cleaned_list[x][0], int(cleaned_list[x][-1])
    # if result[1]=="o" #identify if it doesn't return lines of breakpoints
    #     print("no breakpoints found")
    #     return
    #print("breakpoints returns: ", num_and_line)
    return cleaned_list




def refresh_new_vars():
    global var_list
    #new_vars=handle("info locals")
    myVars=handle("info locals")
    #myVars=myVars[1:-1]
    #print(myVars)
    j=0
    vars.erase()
    vars.addstr(" Variables:\n")
    for vari in myVars:
        if vari["type"]!="console":
            pass
        else:
            j+=1
            #global local_vars
            vari=vari["payload"].strip()
            #var_list[j]=vari
            vars.addnstr(j, 1, vari, half_width-2)
    vars.noutrefresh()
    #print(v_count)
    #print("var count: ", v_count)
    #print(local_vars)
    #refresh_vars(local_vars)
   

def refresh_all(): #use instead of getch/individual pad refreshes to keep eveerything updating on screen at the same time
    win_update() #updates inferior code scrolling
    reg_update()
    #print(local_vars)
    refresh_new_vars()
    #print_commands()
    #refresh_vars(local_vars, v_count)

    #code_trace.noutrefresh(trace_scroll, 0,0, int(width/2),(height-5), (width-2))  #upper-left(y,x)of pad, upper-left(y,x) of window, lower-right corner(y,x) 
    #code_trace.noutrefresh()  #upper-left(y,x)of pad, upper-left(y,x) of window, lower-right corner(y,x) aka: this onlien guide scrollY, scrollX, posY, posX, sizeY, sizeX
    #vars.noutrefresh(0,0,0,0, int(height/2), int(width/2)) #(scroll, 0, 0, 0, maxy, maxx)
    curses.doupdate() 

def temp_refresh():
    refresh_vars()
    reg_update()
    win_update()
    curses.doupdate()

def refresh_vars(variables): #check if same or not and erase accordingly boo
    global var_list
    for j in var_list[:half_height]:
        vars.addnstr(j+1, 1, var_list[j], half_width-2)
    #variables=variables.split('\n')
    #for z, line in enumerate(var_list[:half_height]) :
        #vars.addnstr(z+1, 1, line, half_width-2) #add up to 2 items
        #except Exception as e:
            #print(e)
        #vars.addstr(local_vars[y])
    vars.noutrefresh() 


def win_update():
    global myInferior #if a file is entered
    code_win.erase()
    #print("enter win update")
    f=open(myInferior)
    myLines=f.readlines() 
    inf_h=len(myLines)-1 #read current line instead maybe split the boys instead of read lines
    #print(inf_h)
    global trace_scroll
    if trace_scroll > (inf_h):
        trace_scroll=inf_h
    myLines=myLines[trace_scroll: inf_h+1]
        #print(myLines)
    y=0
    for line in myLines:
             #bold the active line
        if y==trace_scroll:
            code_win.addnstr(y,1,line,half_width-2, curses.A_STANDOUT)
        elif line!='':
            code_win.addnstr(y, 1, line, half_width-2)
        y+=1

            #for w in range(line_len):
                #code_win.addch(y,w, myLines[y][w])
                #if y>= height or w>= half_width:
                    #print("inferior window out of range")
                #if y==trace_scroll: #a_bold or a_standout
                    #code_win.addch(y, w, myLines[y][w], curses.A_STANDOUT) #add strandout spaces for the rest of the line?
                #elif isinstance(myLines[y][w], str):
                    #try:
                        #code_win.addch(y, w, myLines[y][w])
                    #except Exception as e:
                        #print("inferior code line print update error: ", e, height-1,  y, w, myLines[y][w])
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

def reg_update():
    this=handle('info registers')
    for i in range(len(this)):
        this[i]=str(this[i]["payload"])
    
    this=[r for r in this if r.startswith("r")]
    dbInfo.erase() #erase this section
    dbInfo.addstr(" Registers:\n", curses.A_BOLD) #add header
    y=half_height+2 #index height of the pane
    for r in this:
        dbInfo.addstr(" "+str(r))
        y+=1
        if y>=height-3:
            return
    dbInfo.noutrefresh()

    #for r in this:
        #r=r.split()
        #if r[0]=="r":
            #print(r)
def print_commands():
    visible_cmds.addstr("N: next line | B: new breakpoint | C: continue to breakpoint | Q: quit")
    visible_cmds.noutrefresh()

def print_bp():
    show_bp.erase() #clear window
    text="Current Breakpoint: "+str(b_list)
    show_bp.addstr(text)
    show_bp.noutrefresh()


#Init file stuff 
f=input("GDBaby\nEnter an Executable Filename: ")
#f="a.out" #replace
handle("-file-exec-and-symbols " + str(f))
result=handle("-exec-run --start") #run and set initial breakpoint
#handle("-exec-run")
myInferior=str(result[0]["payload"]["bkpt"]["file"])
trace_scroll=int(result[0]["payload"]["bkpt"]["line"])
#check_inferior() #set inferior file, update scroll pos
b_list=str(trace_scroll)
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
vars = curses.newwin(half_height-1, half_width, 0, 0) #(height, width, begin_y, begin_x)
dbInfo = curses.newwin(half_height-1, half_width, int(height/2)+1, 0) #(height, width, begin_y, begin_x)
code_win= curses.newwin(height-2, half_width-2, 0, half_width+2)
visible_cmds=curses.newwin(1, half_width-1, height-1, half_width+int((half_width-60)/2))
show_bp=curses.newwin(1, half_width-1, height-1, 0)
#local_vars=local_vars.split('\n')
#local_vars=handle("info locals")
#trace_scroll=0

#win_update()
#visible_cmds.addstr("n:Next line b:Set Breakpoint")
#visible_cmds.noutrefresh()
stdscr.refresh() #updates screen upon launching rather than waiting for keystroke
check_inferior()
print_commands()
#b_list=get_breakpoints()
print_bp()
refresh_all() #refresh all panes. *****

while True:
    #print("in user control function! ")
    #global b_list
    #global trace_scroll
    if b_list!="": #looping breakpoint
        breakpoint="break"+str(b_list)
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
        win_update()
        curses.doupdate()
    elif c == curses.KEY_DOWN: #scroll input code down
        trace_scroll+=1
        #refresh_all()
        win_update()
        curses.doupdate()
    ch = chr(c) #chr(ascii_val) becomes a letter
    #if ch=='r':
        #out=handle_go("run") #already in start boo
        #dbInfo.addstr(out)
        #dbInfo.noutrefresh()
        #refresh_all()
    if ch=='n': #next line
        #print("next")
        result=handle("next")
        #result=result[0]
        #print(result)
        for i in result:
            if i["type"]=="notify" and i["message"]=="stopped":
                trace_scroll=int(i["payload"]["frame"]["line"])
    
            #trace_scroll=int(result)
            #print("next result: " , repr(result), result)
        #check_inferior()
            #refresh_new_vars()
            #reg_update()
            #refresh_all()
            #win_update()
            #trace_scroll=5
        refresh_all()
        #print(result)
        #refresh_all()
    elif ch=="c":
        result=handle("continue")
        dbInfo.erase()
        refresh_new_vars()
        dbInfo.addstr("Output:\n")
        for i in result:
            if i["type"]=="output":
                dbInfo.addstr(i["payload"]+"\n") 
        dbInfo.noutrefresh()
        trace_scroll=int(b_list)
        win_update()
        curses.doupdate()
        #result=handle("frame")
        #print(result)
        print(myInferior)
        handle("-file-exec-and-symbols "+str(myInferior))
        handle("break "+str(b_list))
        result=handle("-exec-run --start")
        #print(result)
        check_inferior()
        #print(result)
        #refresh_all()
    elif ch=='b':
        handle("clear")
        b_list=str(trace_scroll)
        breakpoint="break"+str(b_list)
        out=handle(breakpoint)
        print_bp()
        refresh_all()
    #elif ch=='m': #display registers

    elif ch == 'q': #113:'q' in ascii
        exit_curses()


#start real gdb stuff. I am the inferior program :( The debugged)
#set startup-with-shell off #disable external shell? current error? gdb issue?
#gdb 
#handle all print
