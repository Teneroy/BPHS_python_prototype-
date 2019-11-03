from Queue import Queue
from threading import Thread
from threading import RLock
import time
lock = RLock()

class MyThread1(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.data = 1

    def getData(self):
        return self.data

    def run(self):
        count = 0
        while True:
            count += 1


class MyThread2(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.data = 'a'

    def getData(self):
        return self.data

    def run(self):
        count = 0
        while True:
            count += 1

class Display(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.data = None

    def display(self, data):
        lock.acquire()
        self.data = data
        lock.release()

    def run(self):
        while True:
            #time.sleep(2)
            lock.acquire()
            if self.data == 'a':
                print 'Thread2 ', self.data
            elif self.data == 1:
                print 'Thread2 ', self.data
            lock.release()


print "checkpoint1"
qu = Queue()
print "checkpoint2"
thread1 = MyThread1()
thread2 = MyThread2()
display_thread = Display()
print "checkpoint3"
thread1.start()
thread2.start()
display_thread.start()
print thread1.getData()
print thread2.getData()
print "checkpoint4"
qu.put(thread1.getData())
qu.put(thread2.getData())
print "checkpoint5"
while not qu.empty():
    print qu.get()
print "checkpoint6"


while True:
    qu.put(thread1.getData())
    qu.put(thread2.getData())
    time.sleep(5)
    display_thread.display(qu.get())

thread1.join()
thread2.join()
display_thread.join()