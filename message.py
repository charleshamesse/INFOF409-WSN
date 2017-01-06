class Message:
    def __init__(self, header, origin):
        self.header = header
        self.origin = origin
        self.path = [origin]
        self.failed = False
        self.passed = False

    def transfer(self, n):
        self.path.append(n)

    def fail(self):
        self.failed = True

    def success(self):
        self.passed = True

    def describe(self):
        return 'Message ' + self.header + '\t ' + str(self.path)