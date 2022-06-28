"""
Using the offical rules
SOURCE: https://tetris.fandom.com/wiki
"""

officalLevelCycles = {
    0 :	48,
    1 :	43,
    2 :	38,
    3 :	33,
    4 :	28,
    5 :	23,
    6 :	18,
    7 :	13,
    8 :	 8,
    9 :	 6,
    10:  5,
    11:  5,
    12:	 5,
    13:  4,
    14:  4,
    15:  4,
    16:  3,
    17:  3,
    18:  3,
    19:  2,
    20:  2
}
def officalScoreSystem(numOfRows, level): return (40*numOfRows)*(level + 1)
officalLevelRowsToClear = {
    0 :	 10,
    1 :	 20,
    2 :	 30,	
    3 :	 40,	
    4 :	 50,	
    5 :	 60,	
    6 :	 70,	
    7 :	 80,	
    8 :	 90,	
    9 :	100,
    10:	100,
    11:	100,
    12:	100,
    13:	100,
    14:	100,
    15:	100,
    16:	110,
    17:	120,
    18:	130,
    19:	140,
    20:	150,
    21:	160,
    22:	170,
    23:	180,
    24:	190,
    25:	200,
    26:	200,
    27:	200,
    28:	200
}