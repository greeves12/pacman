import time
import threading

class Timer():
    time = 0
    thread = None
    tick = False
    breakThread = False

    def __init__(self, time):
        self.time = time

    def kill_thread(self):
        self.breakThread = True

    def start_timer(self):
        self.thread = threading.Thread(target=self.__start_timer2)
        self.thread.start()
    
    def __start_timer2(self):
        while True:
            if self.breakThread:
                break

            self.tick = False
            time.sleep(self.time)
            self.tick = True
            time.sleep(self.time)

    def get_status(self):
        return self.tick