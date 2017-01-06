class Message:
    def __init__(self, header, origin):
        self.header = header
        self.origin = origin
        self.path = [origin]

    def transfer(self, n):
        self.path.append(n)

    def describe(self):
        return 'Message ' + self.header + '\t ' + str(self.path)