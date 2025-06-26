from PIL import Image, ImageDraw, ImageFont
import datetime
import os
import json

from card import Troublecard

class CardRenderer:
    def __init__(self, asset_dir='cardpack'):
        self.asset_dir = asset_dir
        self.info = json.load(open(os.path.join(asset_dir, 'info.json')))
        self.font = ImageFont.truetype(os.path.join(asset_dir, self.info['labelfont']), self.info['labelsize'])


    def render_card(self, card:Troublecard, side='front', holesize=15):
        now = datetime.datetime.now()
        punchdate = now.strftime("%y-%m-%d_%H-%M")
        bits = card.bits
        im=Image.open(os.path.join(self.asset_dir, self.info['images'][side]))

        label_data = {
            'id': card.id.string(),
            'date': card.timestamp,
            'punchdate': punchdate,
            'office': "Duwamish",
            'month': now.strftime("%m"),
            'year': now.strftime("%Y"),
            'smalldate': now.strftime("%m/%d"),
            'smalltime': now.strftime("%H:%M"),
        }

        origin_x, origin_y = self.info['offsets'][side]['origin']
        offset_x, offset_y = self.info['offsets'][side]['offset']

        draw = ImageDraw.Draw(im)
        
        for xidx in range(69):
            for yidx in range(18):
                if xidx>30 and xidx<38: continue
                #Don't tell Professor Mead, these numbers are magic
                xcen=origin_x+(xidx*offset_x) 
                ycen=origin_y+(yidx*offset_y)
                #It's hole-punchin' time
                if bits[yidx][xidx]:
                    draw.circle((xcen, ycen), holesize, 'black')
        
        for name,xpos,ypos in self.info['offsets'][side]['labels']:
            print(name, label_data[name],xpos,ypos)
            draw.text((xpos, ypos), label_data[name], font=self.font, fill='red')
            
        rgb_im  = im.convert('RGB')

        return rgb_im
