from pygame import *
class scroll(object):
    def __init__(self,screen, text, c=(0,0,255),speed=15):
        font.init()
        self.surf,self.text,self.c,self.x,self.dy,self.font = screen,text,c,100,35+speed,(font.Font("ReturnofGanon.ttf", 35))
        self.screen = self.surf.subsurface((168,454,464,286))
        self.height = screen.get_rect().bottom
        self.offset,self.text_height = 445,(len(self.text) * self.dy)
        self.textrect = (168,454,464,286)
    def run(self):
        y = self.offset
        for line in self.text:
            self.render(line,self.x,y)
            y+=self.dy
    def render(self,text,x=50,y=0):
        surface = self.font.render(text,True,self.c)
        surfacerect = surface.get_rect()
        surfacerect.centerx = self.screen.get_rect().centerx
        self.screen.blit(surface,(surfacerect.x,y))
