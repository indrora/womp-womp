# Analysis of trouble card data
import enum
from card import Troublecard

class Field:
    def __init__(self, coords:tuple, name:str, description:str):
        self.coords = coords
        print(self.coords)
        self.name = name
        self.description = description
    
    def extract(self, card:Troublecard) -> tuple:
        x,y = self.coords
        return ( card.bits[y][x], None)

class TwoOfFiveField(Field):

    def extract(self, card:Troublecard) -> tuple:
        x,y = self.coords
        return ( get_2of5(card.bits[y][x:x+5]), None)


fields = [
    Field((0,0), "TI", "Trouble Indication"),
    Field((19, 0), "DR0", "Display Registered"),
    Field((20, 0), "DR1", "Display Registered"),
    Field((21, 0), "DR2", "Display Registered"),
    Field((22, 0), "DR3", "Display Registered"),
    Field((23, 0), "DR4", "Display Registered"),
    Field((24, 0), "DR5", "Display Registered"),
    Field((25, 0), "DR6", "Display Registered"),
    Field((26, 0), "DR7", "Display Registered"),
    Field((27, 0), "DR8", "Display Registered"),
    Field((28, 0), "DR9", "Display Registered"),

    # WT, SDT, LDT, TRS, TGT, FCG, LR, DCK, GT5, SQA, PSR
    Field((2, 1), "WT", "Work Timer"),
    Field((3, 1), "SDT", "Short Delay Timer"),
    Field((4, 1), "LDT", "Long Delay Timer"),
    Field((5, 1), "TRS", "Transfer Start"),
    Field((6, 1), "TGT", "Trunk Guard Test"),
    Field((7, 1), "FCG", "False Cross Ground"),
    Field((8, 1), "LR", "Link Release"),
    Field((9, 1), "DCK", "Double Connection Check"),
    Field((10, 1), "GT5", "Ground Test"),
    Field((11, 1), "SQA", "Sequence Advance"),
    Field((12, 1), "PSR", "Permanent Signal Record"),

    # ITR, SOG, TER, TOG
    Field((16, 1), "ITR", "IntraOffice"),
    Field((17, 1), "SOG", "Subscriber OutGoing"),
    Field((18, 1), "TER", "Terminating"),
    Field((19, 1), "TOG", "Toll-Tandem Outgoing"),

    Field((0, 3), "FR0", "Connector Frame"),
    Field((1, 3), "FR1", "Connector Frame"),

    Field((0, 4), "CN-RG0", "Connector Register 0"),
    Field((1, 4), "CN-RG1", "Connector Register 1"),
    Field((2, 4), "CN-RG2", "Connector Register 2"),
    Field((3, 4), "CN-RG3", "Connector Register 3"),
    Field((4, 4), "CN-RG4", "Connector Register 4"),
    Field((5, 4), "CN-RG5", "Connector Register 5"),
    Field((6, 4), "CN-RG6", "Connector Register 6"),
    Field((7, 4), "CN-RG7", "Connector Register 7"),
    
    # OR FAC INC TAN TOL
    Field((10, 5), "OR", "Originating Register"),
    Field((11, 5), "FAC", "Direct Dial Long-Distance"),
    Field((12, 5), "INC", "Incoming"),
    Field((13, 5,), "TAN", "Tandem"),
    Field((14, 5), "TOL", "Toll"),

    # LT1 LT2 LT3 _ RO
    Field((20, 5), "LT1", "LT1"),
    Field((21, 5), "LT2", "LT2"),
    Field((22, 5), "LT3", "LT3"),
    Field((24, 5), "RO", "Reorder")
]


def analyze_card(card:Troublecard):

    analysis = {}

    for field in fields:
        value,err = field.extract(card)
        analysis[field.name] = value

    return analysis


def map_fields(bits, fields):
    if len(bits) != len(fields):
        raise ValueError("Expected %d bits, got %d" % (len(fields), len(bits)))
    ret = []
    for i in range(len(bits)):
        if bits[i]:
            ret.append(fields[i])
    return ret


def get_2of5(bits):
    if len(bits) != 5:
        raise ValueError("Expected 5 bits")
    vals = [0,1,2,4,7]
    num = 0
    for i in range(5):
        if bits[i]:
            num += vals[i]
    return num

def map_2of5(bits):
    # for each 5 bits, map to a number:
    if len(bits) % 5 != 0:
        raise ValueError("Expected multiple of 5 bits")
    nums = []
    for i in range(0, len(bits), 5):
        nums.append(get_2of5(bits[i:i+5]))
    return nums

