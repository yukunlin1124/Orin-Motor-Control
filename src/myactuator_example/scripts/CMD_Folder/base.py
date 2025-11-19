class CommandGenerator:
    def __init__(self):
        self.cmd_value = 0

    def get(self, t):
        raise NotImplementedError

    def print(self, t):
        cmd_value = self.get(t)
        print("At time {:.2f}, command value is {:.2f}".format(t, cmd_value))
        return cmd_value

