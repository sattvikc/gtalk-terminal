import os, pty, thread, sys, time, fcntl, signal

class PySSH:
    def __init__(self, host="localhost", username="root"):
        (self.master, self.slave) = pty.openpty()
        (self.pid, self.fd) = pty.fork()
        if self.pid == 0:
            pty.spawn(["ssh", "%s@%s" % (username, host)], self.master_read, self.slave_read)
        else:
            attr = fcntl.fcntl(self.fd, fcntl.F_GETFL)
            attr |= os.O_NONBLOCK
            fcntl.fcntl(self.fd, fcntl.F_SETFL, attr)
            self.outputLock = thread.allocate_lock()
            self.running = True
            self.outputText = ""
            self.outputPresent = False
            thread.start_new_thread(self.keepReading, ())
    
    def startCommand(self, cmd):
        #pid = os.fork()
        os.write(self.fd, cmd)
    
    def keepReading(self):
        while(1):
            finish = 0
            while self.running:
                try:
                    data = os.read(self.fd, 1024)
                    break
                except:
                    time.sleep(1)
            self.outputLock.acquire()
            while 1:
                self.outputText += data
                try:
                    data = os.read(self.fd, 1024)
                except:
                    break
            self.outputPresent = True
            self.outputLock.release()
            
    def readOutput(self):
        self.outputLock.acquire()
        data = self.outputText
        self.outputText = ""
        self.outputPresent = False
        self.outputLock.release()
        return data
    
    def master_read(self, masterfd):
        #os.write(self.fd, raw_input() +"\n")
        data = os.read(masterfd, 1024)
        #print "Data:",data
        return data

    def slave_read(self, slavefd):
        #os.write(self.fd, raw_input() +"\n")
        data = os.read(slavefd, 1024)
        #print "Data:",data
        return data
        
    def close(self):
        self.running = False
        os.kill(self.pid, signal.SIGQUIT)

#def readFromShell(shell):
#    while a.running:
#        if a.outputPresent:
#            sys.stdout.write(a.readOutput())
#            sys.stdout.flush()
#        else:
#            time.sleep(1)
#a = PyShell()
#thread.start_new_thread(readFromShell, (a,))
#while(1):
#    cmd = raw_input("")
#    a.startCommand(cmd+"\n")
#    if cmd=="exit": break
#    time.sleep(1)
#    
#a.close()
