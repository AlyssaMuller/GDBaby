#!/usr/bin/env python
# encoding: utf-8
#    gdb -ex 'source gdbcontrol.py' -ex 'ask'

import gdb

def load(f):
    gdb.execute("file " + str(f))  # get file
    fin=open(f, "r")
    print(str(fin))
    fin.close()



def tokenizer(cmd):
    if cmd==b:
        cmd='break main'
    elif cmd==c:
        cmd='continue'
    elif cmd==d:
        cmd='delete main'
    elif cmd==i:
        cmd='info breakpoints'
    elif cmd==s:
        cmd="step"
    elif cmd==r:
        cmd="run"
    elif cmd==v:
        cmd="info locals"

def handle(cmd):
    gdb.execute(cmd, to_string=True)

def error():
    print("Error Occurred: ", gdb.error)
    return

def main():
    f=input("enter a executable filename: ")
    load(f)
    cmd=input("enter a command: ")
    handle(cmd)


if __name__ == "__main__":
    main()