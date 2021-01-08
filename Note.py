

class Note:

    xPosition: int
    yPosition: int
    notation: str
    duration: int
    accidental: str
    numBeams: int
    numDots: int

    def __init__(self, x, y, notation, dur, acc=''):
        self.xPosition = x
        self.yPosition = y
        self.notation = notation
        self.duration = dur
        self.accidental = acc
        self.numBeams = 0
        self.numDots = 0

    def __str__(self):
        if self.duration == 1:
            Type = 'Whole'
        elif self.duration == 2:
            Type = 'Half'
        elif self.duration == 4:
            Type = 'Quarter'
        elif self.duration == 8:
            Type = 'Eigth'
        elif self.duration == 16:
            Type = 'Sixteenth'
        elif self.duration == 32:
            Type = 'Thirty Second'
        else:
            Type = 'LOL'
        string = 'X: ' + str(self.xPosition) + '  '
        string += 'Y: ' + str(self.yPosition) + '  '
        string += 'Notation: ' + self.notation + self.accidental + '/' + str(self.duration) + self.numDots*'.' + '  '
        string += 'Type: ' + Type 

        return string
        