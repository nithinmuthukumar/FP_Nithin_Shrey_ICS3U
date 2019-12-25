from pygame import *
from imageload import imageload
from ScrollTextClass_and_OpeningCredits import scroll		#scrolling text class
class Credits():
    def __init__(self):
        self.screen = display.set_mode((800,740))	#Credits Screen -- Display Initalization
        self.creditsBG = imageload("images/Backgrounds/CreditsBG.png",1,False,(255,255,255))	#Background of the credits page
        self.credit = open("credits.txt").read().strip().split("\n")	#creates a list of each line from the text file
        self.closing = scroll(self.screen,self.credit,(200,255,0))		#creates scrolling text class instance
        self.clock = time.Clock()	#Creates clock for text movement rate
        self.done = False
    def run(self):
        while not self.done:
            for e in event.get():
                if e.type==QUIT:
                    self.done = True
            self.milliseconds = self.clock.tick(60)		#milliseconds passed per second
            self.closing.offset -= self.milliseconds / 25 #vertical movement -- decrease to go faster
            if self.closing.offset * -1 > self.closing.text_height:	#if the height of all the lines together is less then the where the text ends (at top of screen - 10 in this case)
            														#i.e. if the bottom of the text block scrolls up past the offset given (but this time the offset is from the top)
                self.done = True
                from Menu import menu
                menu()		#brings you back to the main menu after credits play
            self.screen.blit(self.creditsBG,(0,0))	#blit the background
            self.closing.run()		#run the instance of the scrolling text class
            display.flip()
        quit()


