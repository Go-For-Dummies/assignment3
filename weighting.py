import re

class WeightUtil:

    def __init__(self, file):

        file1 = open(file, 'r')
        weightlist = file1.readlines()
        self.weightdict = {}
        for line in weightlist:
            splitline = re.split(" ", line)
            index, weight = splitline
            self.weightdict[index] = weight

    def getweight(self, index):
        """
        Takes a base 4 index string and returns a weight for that move
        """
        indexb10 = str(int(index, 4))
        return self.weightdict[indexb10]

