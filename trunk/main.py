#!/usr/bin/env python
from pyssh import PySSH
import thread, sys, time

def readFromShell(shell):
    while a.running:
        if a.outputPresent:
            sys.stdout.write(a.readOutput())
            sys.stdout.flush()
        else:
            time.sleep(1)

if(len(sys.argv) != 3):
    print "Usage: %s <hostname> <username>" % sys.argv[0]
    sys.exit(1)

a = PySSH(sys.argv[1], sys.argv[2])
thread.start_new_thread(readFromShell, (a,))

while(1):
    cmd = raw_input("")
    a.startCommand(cmd+"\n")
    if cmd=="exit": break
    time.sleep(1)
a.close()