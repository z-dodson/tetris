"""
Tetris clone in pygame
"""
import pygame
import random
import sys
from colours import *
from datastructures import *
from matrix import Matrix
import math as maths
from rules import *
from pygame.locals import K_DOWN, K_LEFT,K_RIGHT
SQ_WIDTH = 20
SQ_HEIGHT = SQ_WIDTH
WIDTH_MARGIN = 130
HEIGHT_MARGIN = 100
WIDTH = SQ_WIDTH*10+WIDTH_MARGIN*2
HEIGHT = SQ_HEIGHT*20+HEIGHT_MARGIN*2
M_WIDTH = int(SQ_WIDTH//2)# m refering to marker
M_HEIGHT = int(SQ_HEIGHT//2)
GAP = 1

BACKGROUND = (20,20,20)
clockwiseTransformation = Matrix(
    [0,-1],
    [1, 0]
)
anticlockwiseTransformation = Matrix(
    [0, 1],
    [-1,0]
)
# cos -sin
# sin  cos
class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, white):
        super().__init__()
        self.image = pygame.surface.Surface([SQ_WIDTH,SQ_HEIGHT])
        self.rect = self.image.get_rect()
        self.image.fill(BLACK)
        self.rect.x = x
        self.rect.y = y
        squares.add(self)
        allsprites.add(self)

class Piece(pygame.sprite.Sprite):
    """Base class for almost all pieces except the rather unusal long block and square block which need some modifyting"""
    def __init__(self,colour) -> None:
        self.colour = colour
        self.blockImg = pygame.Surface(((2*GAP)+SQ_WIDTH,(2*GAP)+SQ_HEIGHT))
        self.blockImg.fill(WHITE) 
        img = pygame.Surface((SQ_WIDTH,SQ_HEIGHT))
        img.fill(colour)
        self.blockImg.blit(img, (GAP,GAP))
        self.drawImage()
        self.rect = self.image.get_rect()
        self.xPos, self.yPos = 3, 0
        self.update()

    def rotate(self): 
        """Actually does the rotation"""
        # Rotation
        self.choords = (clockwiseTransformation*self.choords.transpose()).transpose()
        if not MAP.checkPoints(*self.convertToPoints()): self.drawImage()
        else: self.choords = (anticlockwiseTransformation*self.choords.transpose()).transpose()


    
    def drawImage(self):
        self.image = pygame.Surface((GAP+3*(GAP+SQ_WIDTH),GAP+3*(GAP+SQ_HEIGHT)), pygame.SRCALPHA, 32)
        for coord in self.choords: self.image.blit(self.blockImg, ((coord[0]+1)*(SQ_WIDTH+GAP),(coord[1]+1)*(SQ_WIDTH+GAP)))

    def convertToPoints(self):
        n = []
        for point in self.choords: n.append([(point[0]+self.xPos+1),(point[1]+self.yPos+1)])
        return n
    def convertToRelativePoint(self,point):
        return [(point[0]-self.xPos-1),(point[1]-self.yPos-1)]
    def moveLeft(self): 
        self.xPos -= 1 
        if not MAP.checkPoints(*self.convertToPoints()): self.drawImage()
        else: self.xPos += 1
    def moveRight(self):
        self.xPos += 1 
        if not MAP.checkPoints(*self.convertToPoints()): self.drawImage()
        else: self.xPos -= 1
    def moveDown(self):
        self.yPos += 1
        if not MAP.checkPoints(*self.convertToPoints()): return False
        else: 
            self.yPos -= 1
            return True
    def shootDown(self): 
        stopped = None
        while not stopped: stopped = self.moveDown()
    def update(self):
        self.rect.x =  WIDTH_MARGIN+self.xPos*(GAP+SQ_WIDTH)-GAP
        self.rect.y = HEIGHT_MARGIN+self.yPos*(GAP+SQ_WIDTH)-GAP
    def __eq__(self, other) -> bool:
        if self.which==other.which: return True
        return False
    def reset(self): return self.__init__()
    def removePoints(self, row):
        for point in self.convertToPoints():
            if point[1]==row: self.choords.remove(self.convertToRelativePoint(point))
            if point[1] >row: 
                self.choords.replace(self.convertToRelativePoint(point), self.convertToRelativePoint([point[0],point[1]-1]))
        self.drawImage()
    def drop(self, row):
        if self.yPos<=row: 
            self.yPos += 1
            self.update()
    def getImage(self):
        o,l,d = self.xPos, self.yPos, self.choords
        self.shootDown()
        x,y,m= self.xPos, self.yPos, self.choords
        self.xPos, self.yPos, self.choords = o,l,d
        return x,y,m, self.which

            
class Piece1(Piece):
    """
    # - -
    # # #
    - - -
    """
    def __init__(self) -> None:
        self.which = 1
        self.choords = Matrix([-1,-1],[-1,0],[0,0],[1,0])
        super().__init__(BLUE)
class Piece2(Piece):
    """
    - - #
    # # #
    - - -
    """
    def __init__(self) -> None:
        self.which = 2
        self.choords = Matrix([1,-1],[-1,0],[0,0],[1,0])
        super().__init__((255,165,0))
class Piece3(Piece):
    """
    # # -
    - # #
    - - -
    """
    def __init__(self) -> None:
        self.which = 3
        self.choords = Matrix([-1,-1],[0,-1],[0,0],[1,0])
        super().__init__(RED)
class Piece4(Piece):
    """
    - # #
    # # -
    - - -
    """
    def __init__(self) -> None:
        self.which = 4
        self.choords = Matrix([1,-1],[-1,0],[0,0],[0,-1])
        super().__init__(GREEN)
class Piece5(Piece):
    """
    - # -
    # # #
    - - -
    """
    def __init__(self) -> None:
        self.which = 5
        self.choords = Matrix([0,-1],[-1,0],[0,0],[1,0])
        super().__init__((138,43,226))
class Piece6(Piece):
    """
    # #
    # #
    """
    def __init__(self) -> None:
        self.which = 6
        self.choords = Matrix([-1,-1],[-1,0],[0,0],[0,-1])
        super().__init__(YELLOW)
    def rotate(self):
        pass
class Piece7(Piece):
    """
    - # - -
    - # - -
    - # - -
    - # - -
    """
    def __init__(self) -> None:
        self.which = 7
        self.choords = Matrix([1.5,-0.5],[0.5,-0.5],[-0.5,-0.5],[-1.5,-0.5])
        super().__init__((0,255,255))
    def drawImage(self):
        self.image = pygame.Surface((GAP+4*(GAP+SQ_WIDTH),GAP+4*(GAP+SQ_HEIGHT)), pygame.SRCALPHA, 32)
        for coord in self.choords: self.image.blit(self.blockImg, ((coord[0]+1.5)*(SQ_WIDTH+GAP),(coord[1]+1.5)*(SQ_WIDTH+GAP)))
    def convertToPoints(self):
        n = []
        for point in self.choords: n.append([(point[0]+self.xPos+1.5),(point[1]+self.yPos+1.5)])
        return n
    def convertToRelativePoint(self,point):
        return [(point[0]-self.xPos-1.5),(point[1]-self.yPos-1.5)]
        


def drawStuff(screen):
    screen.blit(PIECES_QUEUE1.image,(350,100))
    screen.blit(PIECES_QUEUE2.image,(350,150))
    screen.blit(PIECES_QUEUE3.image,(350,200))
    if CACHED_PIECE: screen.blit(CACHED_PIECE.image, (30,100))
class Randomiser:
    def __init__(self) -> None: self.bag = [Piece1,Piece2,Piece3,Piece4,Piece5,Piece6,Piece7]
    def random_piece(self):
        if not self.bag:
            self.bag = [Piece1,Piece2,Piece3,Piece4,Piece5,Piece6,Piece7]
            random.shuffle(self.bag)
        n = self.bag[0]
        self.bag.pop(0)
        return n()
class Image(Piece):
    def __init__(self) -> None:
        self.blockImg = pygame.Surface(((2*GAP)+SQ_WIDTH,(2*GAP)+SQ_HEIGHT))
        self.blockImg.fill(WHITE) 
        img = pygame.Surface((SQ_WIDTH-4*GAP,SQ_HEIGHT-4*GAP))
        img.fill(BLACK)
        self.blockImg.blit(img, (GAP*3,3*GAP))
    def setPos(self,x,y,matrix,which):
        self.choords = matrix
        self.xPos = x
        self.yPos = y
        if which == 7:
            self.image = pygame.Surface((GAP+4*(GAP+SQ_WIDTH),GAP+4*(GAP+SQ_HEIGHT)), pygame.SRCALPHA, 32)
            for coord in self.choords: self.image.blit(self.blockImg, ((coord[0]+1.5)*(SQ_WIDTH+GAP),(coord[1]+1.5)*(SQ_WIDTH+GAP)))
        else:
            self.drawImage()
        self.rect = self.image.get_rect()
        self.update()
    
class GraphicBox(pygame.sprite.Sprite):
    def __init__(self,x,y,colour) -> None:
        super().__init__()
        self.image = pygame.Surface((2*GAP+SQ_WIDTH,2*GAP+SQ_HEIGHT))
        self.image.fill(WHITE) 
        img = pygame.Surface((SQ_WIDTH,SQ_HEIGHT))
        img.fill(colour)
        self.image.blit(img, (GAP,GAP))
        self.rect = (WIDTH_MARGIN+x*(GAP+SQ_WIDTH)-GAP,HEIGHT_MARGIN+y*(GAP+SQ_WIDTH)-GAP)
         

def pause_loop(screen):
    paused = True
    c = (128,128,128)
    clock = pygame.time.Clock()
    while paused:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: done = True
            if event.type == pygame.KEYDOWN: paused = False
        c = ((c[0]+random.randint(0,1))%255,(c[1]+random.randint(0,2))%255,(c[2]+random.randint(0,3))%255)
        screen.fill(c)
        pygame.display.flip()
    return None

class PauseButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(background)
        self.image = pygame.Surface((35,30))
        self.image.fill(WHITE)
        img = pygame.Surface((10,20))
        img.fill(BLACK)
        self.image.blit(img,(5,5))
        self.image.blit(img,(20,5))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 10,10
    def isClicked(self,x,y):
        if self.rect.x<x<self.rect.right and self.rect.y<y<self.rect.bottom: return True
        return False

if __name__=="__main__":
    # Set up
    if 1:
        pygame.init()
        pygame.font.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT),pygame.NOFRAME) 
        squares = pygame.sprite.Group()
        icons = pygame.sprite.Group()
        background = pygame.sprite.Group()
        allsprites = pygame.sprite.Group()
        graphics = []
        backing = pygame.sprite.Sprite()
        backing.image = pygame.surface.Surface([GAP+(SQ_WIDTH+GAP)*10,GAP+(SQ_HEIGHT+GAP)*20])
        backing.rect = backing.image.get_rect()
        backing.rect.x = WIDTH_MARGIN - GAP
        backing.rect.y = HEIGHT_MARGIN - GAP
        backing.image.fill(WHITE)
        background.add(backing)
        holdbox = pygame.sprite.Sprite()
        holdbox.image = pygame.surface.Surface([(WIDTH_MARGIN-GAP*10),SQ_WIDTH*3])
        holdbox.rect = backing.image.get_rect()
        holdbox.rect.x = GAP*5
        holdbox.rect.y = HEIGHT_MARGIN-GAP*5
        holdbox.image.fill(GREY)
        background.add(holdbox)
        queuebox = pygame.sprite.Sprite()
        queuebox.image = pygame.surface.Surface([SQ_WIDTH*5,SQ_HEIGHT*8])
        queuebox.rect = queuebox.image.get_rect()
        queuebox.rect.x = 345
        queuebox.rect.y = 90
        queuebox.image.fill(GREY)
        background.add(queuebox)
        screen.fill(BACKGROUND)
        PAUSE_BUTTON = PauseButton()
        
    white = True
    for i in range(20):
        for j in range(10):
            Square((WIDTH_MARGIN+j*(SQ_WIDTH+GAP)),(HEIGHT_MARGIN+i*(SQ_HEIGHT+GAP)),white)
    allsprites.draw(screen)
    pygame.display.update()
    clock = pygame.time.Clock()
    done = False
    SCORE = 0
    font = pygame.font.SysFont('Arial', 20)
    pygame.display.flip()
    MAP = GroudMap()
    RANDOMISER = Randomiser()
    CURRENT_PIECE = None
    GEN_NEW_PIECE = True
    STORED_PIECE = None
    LEVEL = 0
    PIECES_QUEUE1 = RANDOMISER.random_piece()
    PIECES_QUEUE2 = RANDOMISER.random_piece()
    PIECES_QUEUE3 = RANDOMISER.random_piece()
    CACHED_PIECE = None
    TOTAL_CLEARED_ROWS = 0
    IMAGE = Image()
    cycles = -1
    totalcycles = 0
    while not done:
        cycles += 1
        totalcycles += 1
        clock.tick(60)
        if GEN_NEW_PIECE: 
            # LEVEL CHANGE
            CACHED_ALREADY = False
            GEN_NEW_PIECE = False
            CURRENT_PIECE = PIECES_QUEUE1
            PIECES_QUEUE1 = PIECES_QUEUE2
            PIECES_QUEUE2 = PIECES_QUEUE3
            PIECES_QUEUE3 = RANDOMISER.random_piece()
            while PIECES_QUEUE1==PIECES_QUEUE2==PIECES_QUEUE3:
                PIECES_QUEUE3 = RANDOMISER.random_piece()
        text = font.render(f"Score: {SCORE}", True, RED, WHITE)
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, 10)
        text2 = font.render(f"Level: {LEVEL}", True, RED, WHITE)
        text2Rect = text2.get_rect()
        text2Rect.center = (WIDTH // 2, 40) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE : done = True
                if event.key == pygame.K_SPACE  : 
                    CURRENT_PIECE.shootDown()
                    cycles = officalLevelCycles[LEVEL]
                # if event.key == pygame.K_LEFT  : CURRENT_PIECE.moveLeft()
                # if event.key == pygame.K_RIGHT : CURRENT_PIECE.moveRight()
                # if event.key == pygame.K_DOWN  : CURRENT_PIECE.moveDown()
                if event.key == pygame.K_UP    : CURRENT_PIECE.rotate()
                if event.key == pygame.K_p     : pause_loop(screen)
                if event.key == pygame.K_c     : # Cache piece 
                    if not CACHED_ALREADY:
                        CACHED_ALREADY = True
                        if not CACHED_PIECE: 
                            CACHED_PIECE = PIECES_QUEUE1
                            PIECES_QUEUE1 = PIECES_QUEUE2
                            PIECES_QUEUE2 = PIECES_QUEUE3
                            PIECES_QUEUE3 = RANDOMISER.random_piece()
                        CURRENT_PIECE, CACHED_PIECE = CACHED_PIECE, CURRENT_PIECE
                        CACHED_PIECE.reset()

        keys = pygame.key.get_pressed()
        if keys[K_DOWN]: CURRENT_PIECE.moveDown()
        if keys[K_LEFT]  and totalcycles%5==0: CURRENT_PIECE.moveLeft()
        if keys[K_RIGHT] and totalcycles%5==0: CURRENT_PIECE.moveRight()
        if pygame.mouse.get_pressed()[0]:
            if PAUSE_BUTTON.isClicked(*pygame.mouse.get_pos()): pause_loop(screen)
        if cycles==officalLevelCycles[LEVEL]:
            if CURRENT_PIECE.moveDown(): 
                MAP.occupySquares(CURRENT_PIECE.colour,*CURRENT_PIECE.convertToPoints())
                GEN_NEW_PIECE = True
            cycles = 0
        CURRENT_PIECE.update()
        IMAGE.setPos(*CURRENT_PIECE.getImage())
        rowsDeleted = MAP.update()
        graphics = []
        for y, row in MAP.itterate():
            for x, thing in enumerate(row):
                if thing.occupied: graphics.append(GraphicBox(x,y,thing.colour))
        if rowsDeleted:
            SCORE += officalScoreSystem(len(rowsDeleted),LEVEL)
            TOTAL_CLEARED_ROWS += 1
            if TOTAL_CLEARED_ROWS==officalLevelRowsToClear[LEVEL]:
                LEVEL += 1
                TOTAL_CLEARED_ROWS = 0
        screen.fill(BLACK)
        background.draw(screen)
        squares.draw(screen)
        icons.draw(screen)
        drawStuff(screen)
        screen.blit(text, textRect)
        screen.blit(text2, text2Rect)
        for g in graphics: screen.blit(g.image,g.rect)
        screen.blit(IMAGE.image,IMAGE.rect)
        screen.blit(CURRENT_PIECE.image, CURRENT_PIECE.rect)

        pygame.display.flip()
    pygame.quit()
    sys.exit()
