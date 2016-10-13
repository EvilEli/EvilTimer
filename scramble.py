import random
from datetime import datetime

class CubeTimerScramble():
    def __init__(self):
        self.num_move_map = {0:"U",
                        1:"U'",
                        2:"U2",
                        3:"L",
                        4:"L'",
                        5:"L2",
                        6:"F",
                        7:"F'",
                        8:"F2",
                        9:"R",
                        10:"R'",
                        11:"R2",
                        12:"B",
                        13:"B'",
                        14:"B2",
                        15:"D",
                        16:"D'",
                        17:"D2",
        }
        self.scramble = ""
        self.generateScramble()

    def getNewScramble(self):
        self.generateScramble()
        return self.scramble

    def generateScramble(self):
        lastMove = " "
        self.scramble = ""
        for i in range(25):
            lastMove = self.getRandomMove(lastMove)
            self.scramble += (lastMove + "  ")

    def getRandomMove(self, lastMove):
        random.seed(datetime.now())
        rn = random.randint(0, 17)
        while((self.num_move_map[rn])[0] == lastMove[0]):
            rn = random.randint(0, 17)
        return self.num_move_map[rn]

if __name__ == '__main__':
    cts = CubeTimerScramble()
    print(cts.getNewScramble())
