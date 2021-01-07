

class Note:

    xPosition: int
    yPosition: int
    notation: str
    duration: int

    def __init__(self, x, y, notation, dur):
        self.xPosition = x
        self.yPosition = y
        self.notation = notation
        self.duration = dur

    def __str__(self):
        if self.duration == 1:
            Type = 'Whole'
        elif self.duration == 2:
            Type = 'Half'
        elif self.duration == 4:
            Type = 'Quarter'
        string = 'X: ' + str(self.xPosition) + '  '
        string += 'Y: ' + str(self.yPosition) + '  '
        string += 'Notation: ' + self.notation + '  '
        string += 'Type: ' + Type 

        return string
        