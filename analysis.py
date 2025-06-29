# Analysis of trouble card data

def analyze_card(card:Troublecard):

    analysis = {}
    analysis['TR'] = card.bits[0][0]
    

    pass

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

