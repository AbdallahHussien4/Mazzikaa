class Note:

    xPosition: int
    yPosition: int
    notation: str
    notationP: str
    duration: int
    accidental: str
    numBeams: int
    numDots: int
    ChordStart :int
    ChordEnd :int
    ChordMid :int


    def __init__(self, x, y, notation, notationP, dur, acc=''):
        self.xPosition = x
        self.yPosition = y
        self.notation = notation
        self.notationP = notationP
        self.duration = dur
        self.accidental = acc
        self.numBeams = 0
        self.numDots = 0
        self.ChordStart = 0
        self.ChordEnd = 0
        self.ChordMid = 0

    def inChord(self):
        if (self.ChordStart == 1 or self.ChordMid == 1) and self.ChordEnd==0:
            return True
    
    def __str__(self):

        # if self.duration == 1:
        #     Type = 'Whole'
        # elif self.duration == 2:
        #     Type = 'Half'
        # elif self.duration == 4:
        #     Type = 'Quarter'
        # elif self.duration == 8:
        #     Type = 'Eigth'
        # elif self.duration == 16:
        #     Type = 'Sixteenth'
        # elif self.duration == 32:
        #     Type = 'Thirty Two'
        # else:
        #     Type = 'LOL'

        self.numDots=''  
        #string = 'X: ' + str(self.xPosition) + '  '
        #string += 'Y: ' + str(self.yPosition) + '  '
        if(self.ChordStart==1):
            self.notation="{"+self.notation
            self.numDots= self.numDots+","
        elif (self.ChordEnd==1):
            self.numDots=self.numDots+"}"  
        elif (self.ChordMid==1):
            self.numDots=self.numDots+","     

        #string += 'Notation: ' + self.notation + self.accidental + '/' + str(self.duration) + self.numDots + '  '
        #string += 'Type: ' + Type 
        string =  self.notation +self.accidental+ self.notationP + '/' + str(self.duration) + self.numDots

        return string
        