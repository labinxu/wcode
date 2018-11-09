from threading import Thread
from time import sleep
class Cookbook(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.message = "Hello Parallel Python CookBook"
    def print_message(self):
        print(self.message)
    def run(self):
        print("Thread Starting\n")
        x = 0
        while (x < 5):
            self.print_message()
            sleep(1)
            x += 1
        print('Thread Ended')

print("Process Started")
hello_python = Cookbook()
hello_python.start()
hello_python.join()
print('Process Ended')


