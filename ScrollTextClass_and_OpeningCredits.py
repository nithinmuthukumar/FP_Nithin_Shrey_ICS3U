from pygame import *
from imageload import imageload
#"""
#Class for scrolling text.
#"""
class scroll():
    def __init__(self,screen, text, c=(0,0,255)):
        font.init()		#initialize font
#        """
#        Variables:
#        Screen = surface the text will be blit to
#        text = the list of strings that is the text needed to be blit
##        x = permanent x position (we want the text always centered)
#        dy = by how much the text moves (font size is 35, dy is 50, text should be moving 15 pixels)
#        height = before (beneath) where the text starts
#        offset = where the text starts to show
#        text_height = the height of the entire block of text -- used to determine when the text is finished scrolling
#        	--> multiply the number of lines (len(self.text)) by dy for each line --> total height of text block
#        """
        self.screen,self.text,self.c,self.x,self.dy,self.font = screen,text,c,100,50,(font.Font("ReturnofGanon.ttf", 35))
        self.height = screen.get_rect().bottom
        self.offset,self.text_height = (self.height - 10),(len(self.text) * self.dy)
    def run(self):
        y = self.offset		#what current y position of text line will be
        for line in self.text:	#does text move for each line as a whole
            self.render(line,self.x,y)	#runs through render function to blit the text
            y+=self.dy		#increments to get to the next y value
    def render(self,text,x=50,y=0):
        surface = self.font.render(text,True,self.c)	#generic surface for text
        surfacerect = surface.get_rect()
        surfacerect.centerx = self.screen.get_rect().centerx	#centering each line of text
        self.screen.blit(surface,(surfacerect.x,y))		#bltting text at center, y increment
	#this was just to test the class before importing it into the main credits page

    def play(self):
        screen = display.set_mode((800,740))
        openingBG = imageload("images/Backgrounds/OpeningBG.png",1,False,(255,255,255))
        clock = time.Clock()
 
        story = open("openingcutscene.txt").read().strip().split("\n")
        opening = scroll(screen,story)
        done = False
        while not done:
            for e in event.get():
                if e.type == QUIT:
                    done = True
            milliseconds = clock.tick(60)
            opening.offset -= milliseconds / 25 #vertmovement -- decrease to go faster
            if opening.offset * -1 > opening.text_height:
                done = True
            screen.blit(openingBG,(0,0))
            opening.run()
            display.flip()
 
        return

