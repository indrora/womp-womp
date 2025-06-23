"""
Card management
"""

scanpts_order = [
    [ 7,  6,  5,  4,  3,  2,  1,  0, 'STRA1', 'STR'],
    [15, 14, 13, 12, 11, 10,  9,  8, 'TRC', 'SPL'],
    [23, 22, 21, 20, 19, 18, 17, 16, 'ROS', 'MB'],
    ['BWX1', 'BWX0', 29, 28, 27, 26, 25, 24, 'RSV3.8', 'RSV3.9'],
    [37, 36, 35, 34, 33, 32, 31, 30, 'RSV4.8', 'RSV4.9'],
    [45, 44, 43, 42, 41, 40, 39, 38, 'RSV5.8', 'RSV5.9'],
    [53, 52, 51, 50, 49, 48, 47, 46, 'RSV6.8', 'RSV6.9'],
    [61, 60, 59, 58, 57, 56, 55, 54, 'RSV7.8', 'RSV7.9'],
    [69, 68, 67, 66, 65, 64, 63, 62, 'RSV8.8', 'RSV8.9'],
    [77, 76, 75, 74, 73, 72, 71, 70, 'RSV9.8', 'RSV9.9'],
    [85, 84, 83, 82, 81, 80, 79, 78, 'RSV10.8', 'RSV10.9'],
    [91, 90, 'BWX3', 'BWX2', 89, 88, 87, 86, 'RSV11.8', 'RSV11.9'],
    [99, 98, 97, 96, 95, 94, 93, 92, 'RSV12.8', 'RSV12.9'],
    [107, 106, 105, 104, 103, 102, 101, 100, 'RSV13.8', 'RSV13.9'],
    [115, 114, 113, 112, 111, 110, 109, 108, 'RSV14.8', 'RSV14.9'],
    ['RSV15.0', 'RSV15.1', 'RSV15.2', 'RSV15.3', 119, 118, 117, 116, 'RSV15.8', 'RSV15.9']
    ]

def scan_data_to_card(data):
    card = [[False for x in range(69)] for y in range(18)]


    for scan_group in range(9):
        for i in range(16):
            for j in range(8):
                row = 8 - scan_group
                scanpt_val = scanpts_order[i][j]
                if isinstance(scanpt_val, int):
                    col = scanpt_val % 30
                    if 0 <= scanpt_val and scanpt_val <= 29:
                        row += 9
                    if 30 <= scanpt_val and scanpt_val <= 59:
                        row += 9
                        col += 39
                    if 60 <= scanpt_val and scanpt_val <= 89:
                        pass
                    if 90 <= scanpt_val and scanpt_val <= 119:
                        col += 39
                elif scanpt_val == 'BWX0':
                    col = 30
                    row += 9
                elif scanpt_val == 'BWX1':
                    col = 38
                    row += 9
                elif scanpt_val == 'BWX2':
                    col = 30
                elif scanpt_val == 'BWX3':
                    col = 38

                if (((data[scan_group * 16 + i] >> j) & 1) == 1) and isinstance(scanpt_val, int):
                    if row < 18 and col < 69:
                        # app.logger.debug(f"on iteration s{scan_group} i{i} j{j} got row{row} col{col}")
                        card[row][col] = True
    return card

def print_card(card):
    text = ''
    text += ('+'+('—'*69)+'+\n')
    for y in range(18):
        text += ('|')
        for x in range(69): #nice
            if x==31 or x==37:
                text += ('|')
            elif x>31 and x<37:
                text += (' ')
            else:
                text += ('#' if card[y][x] else '·')
        text += ('|\n')
    text += ('+'+('—'*69)+'+\n')
    return text

def print_cardx(card):
    text = ''
    for y in range(len(card)):
        text += ' '
        print(len(card[y]))
        for x in range(len(card[y])):
            
            if card[y][x]:
                text += '#'
            else:
                text += '·'
        text += '\n'
    return text

def decode_block(data):
    split_data = data.split(',')
    decoded_data = list(map(lambda x: int(x, 16), split_data))
    card = scan_data_to_card(decoded_data)
    return card



if __name__ == "__main__":
    card_block = """0100,0049,0011,0060,0000,0000,0000,0000,0000,0000,0000,0002,0000,0000,0000,0000,0191,00c9,0011,0048,0000,0000,0000,0002,008c,00a2,0094,00a2,0004,0000,0000,0000,0100,0000,0000,0000,0000,0000,0000,000c,0090,0020,0000,0000,0000,0000,0000,0000,0100,0000,0000,0000,0000,0000,0000,0002,0000,0080,0000,0000,0004,0010,0000,0000,0100,0000,0000,0000,0000,0000,0000,0000,0000,0000,0000,0002,0008,0000,0020,0000,0100,0000,0000,0000,0000,0002,0000,0009,0000,0040,0000,0000,0000,0000,0000,0000,0180,0001,0000,0008,0080,0009,0002,0000,0002,0000,0004,0000,0000,0000,0000,0000,0100,0000,0000,0000,0000,0009,0004,0002,0000,0001,0000,0083,00c9,00e0,0000,0010,0150,0040,0000,0000,0000,0040,0000,0000,0000,0004,0020,0013,0017,00ff,0096,0070"""

    card = decode_block(card_block)
    print(print_cardx(card))
    print(print_card(card))