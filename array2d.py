class Array2d:
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__arr = [[0]*width]*height

    def __str__(self):
        out = ""
        for i in range(self.height):
            for j in range(self.width):
                out += str(self.__arr[j][i]) + " "
            out += "\n"
        
        return out        
    
    def fill(self, value):
        for i in range(self.height):
            for j in range(self.width):
                self.__arr[j][i] = value
        
    def at(self, pos):
        return self.__arr[pos[0]][pos[1]]
    
    def set(self, pos, value):
        self.__arr[pos[0]][pos[1]] = value