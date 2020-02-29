
class PrintRedirect:
    def __init__(self, writed):
        self.writed = writed

    def write(self, str):
        self.writed(str)

    def flush(self):
        pass
