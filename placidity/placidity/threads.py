import threading

class Poller:
    def __init__(self, thread_class, interpreter):
        assert hasattr(interpreter, '__call__')

        self.thread_class = thread_class
        self.interpreter = interpreter

    def poll(self):
        self._set_up_thread()

        while True:
            while not self.thread.data_ready.isSet():
                pass

            try:
                self.interpreter(self.thread.data)
            except SystemExit:
                break
            else:
                self._set_up_thread()

    def _set_up_thread(self):
        self.thread = self.thread_class()
        self.thread.start()

class InputThread(threading.Thread):
    def __init__(self):
        self.data_ready = threading.Event()

        super(InputThread, self).__init__()

    def run(self):
        self.data = self.get_data()
        self.data_ready.set()

    def get_data(self):
        pass

class RepeatingTimer:
    def __init__(self, interval, callback):
        def repeat_callback():
            callback()

            if self.running:
                self._timer = self._create_timer()
                self._timer.start()

        self.interval = interval
        self.repeat_callback = repeat_callback

    def start(self):
        self._timer = self._create_timer()
        self.running = True
        self._timer.start()

    def _create_timer(self):
        timer = threading.Timer(self.interval, self.repeat_callback)

        # make sure thread gets killed on app quit
        timer.daemon = True

        return timer

    def cancel(self):
        self.running = False
