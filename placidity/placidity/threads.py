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
