from matrix import *

class GroudMap:
    def __init__(self,width=10,height=20):
        self.width, self.height = width, height
        self.map = [[Square(position,row)for position in range(width)]for row in range(height)]
    def __str__(self) -> str: 
        string = ""
        for row in self.map:
            for thing in row: string += str(thing)
            string += "\n"
        return string
    def checkPoints(self, *points):
        """ Returns ture is occupied"""
        for point in points: # NOTE must input coord in (y,x) form due to how lists work, hence keeping the map in the class so the program dosnt need to messs with this
            if int(point[1])>=len(self.map): return True
            if int(point[0])>=len(self.map[0]): return True
            if int(point[0])<0: return True
            if self.map[int(point[1])][int(point[0])].occupied: return True
        return False
    def occupySquares(self,colour,*points):
        for point in points: self.map[int(point[1])][int(point[0])].occupy(colour)
    def update(self):
        rowstoremove = []
        for index, row in enumerate(self.map):
            if ["#"for _ in range(10)]==[thing.__str__() for thing in row]: 
                rowstoremove.append(index)
                self.map.pop(index)
                for thing in row: thing.moveDown()
                self.map.insert(0,[Square(position,0)for position in range(self.width)])
        return rowstoremove
    def itterate(self):
        for index, row in enumerate(self.map): yield index, row

class Square:
    def __init__(self,x,y,occuplied=False):
        self.x, self.y, self.occupied,self.colour = x, y, occuplied, None
    def __str__(self):
        if self.occupied: return "#"
        return "-"  
    def __repr__(self) -> str: return self.__str__()    
    def occupy(self,colour): self.occupied,self.colour = True, colour
    def moveDown(self): self.y += 1