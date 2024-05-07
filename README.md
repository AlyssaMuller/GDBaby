#GDBaby

Gdbaby is an intuitive debugger meant for minimal set-up. Debuggers are extremely helpful, especially for new programmers that may have no idea where things have gone wrong. At the same time, there is often a barrier to entry surrounding set up, new users often don't know what features would be most helpful to look at or how to achieve them using the software. GDBaby makes the GDB debugger more accessible for users who need the most immediate help. 

GDBaby opens by calling the ./gdbaby file. It will then simply ask for an executable file. This file must be compiled with the -g debugging flag to allow for full debugging purposes. 
[gdb asks](image/startup.png)

It then will gather and set up some basic formatting. This includes viewing the inferior code that is being debugged, and the functionality underneath. The code can be scrolled through as well as basic controls for chnaging what part of the code is to be examined. These uncooked commands are displayed at the bottom for easy access. 
[gdb set up](image/gdbaby.png)
