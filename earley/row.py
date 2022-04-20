class Row:
    def __init__(self, dot, left, right, pos, completes=None):
        self.dot = dot
        self.left = left
        self.right = right
        self.pos = pos
        self.start = pos[0]
        self.end = pos[1]
        self.completes = list() if completes is None else completes

    def show(self):
        dotted = ''.join(self.right)
        formated = (self.left + ' -> ' + ' ' + dotted[:self.dot] +
                    '\033[94m.\033[0m' + dotted[self.dot:])
        if len(formated) < 10:
            formated += '\t'
        formated += '\t\033[93m/'+str(self.start)+'\033[0m'
        print(formated)

    def get_next(self):
        return self.right[self.dot] if self.dot < len(self.right) else None

    def is_complete(self):
        return self.dot == len(self.right)

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right and self.dot == other.dot and self.pos == other.pos
