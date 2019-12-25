from pygame import *
from imageload import imageload

#"""
#Class that displays all the controls in the game.
#"""

class Instructions():
    def __init__(self):
        self.screen = display.set_mode((800,740))	#game display initialization
        font.init()		#font initalization
        self.mx,self.my = 0,0	#need to set mx,my to something because it's referenced before the game loop
        self.hylian = font.Font("ReturnofGanon.ttf",50)		#font used for all text
        self.title = self.hylian.render("Controls",True,(200,255,0))	#title text of the instructions
        self.titlerect = self.title.get_rect()
        self.titlerect.center = self.screen.get_rect().centerx,50		#setting title text position before game loop
#        """
#        The following text renderings are just the controls that correspond with specific images that will be blit onto the screen
#        """
        self.movecontrols = self.hylian.render("Movement................................",True,(200,255,0))
        self.Qcontrol = self.hylian.render("Roll........................................",True,(200,255,0))
        self.Econtrol = self.hylian.render("Backflip..................................",True,(200,255,0))
        self.Jcontrol = self.hylian.render("Boomerang...............................",True,(200,255,0))
        self.Kcontrol = self.hylian.render("Shoot Arrow.............................",True,(200,255,0))
        self.Lcontrol = self.hylian.render("Throw Bomb..............................",True,(200,255,0))
        self.spacecontrols = self.hylian.render("Interact/Swing Sword).................",True,(200,255,0))
        self.gearcontrol = self.hylian.render("Settings (Click With Mouse).........",True,(200,255,0))
        self.mousecontrol = self.hylian.render("Use to Interact With UI...............",True,(200,255,0))
#        """
#        Loading the images for the respective controls that are rendered through text
#        """
        self.instructionsBG = imageload("images/Backgrounds/InstructionsBG.png",1,False,(255,255,255))
        self.WASD = imageload("images/Instructions/WASD.png",0.1,False,(255,255,255))
        self.Q = imageload("images/Instructions/Q.png",1,False,(255,255,255))
        self.E = imageload("images/Instructions/E.png",1,False,(255,255,255))
        self.J = imageload("images/Instructions/J.png",1,False,(255,255,255))
        self.K = imageload("images/Instructions/K.png",1,False,(255,255,255))
        self.L = imageload("images/Instructions/L.png",1,False,(255,255,255))
        self.Spacebar = imageload("images/Instructions/Spacebar.png",0.75,False,(255,255,255))
        self.gear = imageload("images/Instructions/gear.png",0.1,False,(255,255,255))
        self.m = imageload("images/Instructions/mouse.png",0.05,False,(255,255,255))
        self.start = imageload("images/Instructions/Start.png",1,False,(255,255,255))
        self.startHover = imageload("images/Instructions/StartHover.png",1,False,(255,255,255))
        self.startRect = self.start.get_rect()
        self.startRect.center = (self.screen.get_rect().centerx,self.screen.get_rect().bottom-50-25)	#sets the start/continue position before the game loop

    def instructions(self):
#    	"""
#    	Blits all the controls (and corresponding images) to their respective positions
#    	"""
        self.screen.blit(self.title,self.titlerect)
        self.screen.blit(self.movecontrols,(25,125))
        self.screen.blit(self.Qcontrol,(25,175))
        self.screen.blit(self.Econtrol,(25,225))
        self.screen.blit(self.Jcontrol,(25,275))
        self.screen.blit(self.Kcontrol,(25,325))
        self.screen.blit(self.Lcontrol,(25,375))
        self.screen.blit(self.spacecontrols,(25,425))
        self.screen.blit(self.gearcontrol,(25,475))
        self.screen.blit(self.mousecontrol,(25,525))
        self.screen.blit(self.WASD,(605,125))
        self.screen.blit(self.Q,(605,200))
        self.screen.blit(self.E,(605,250))
        self.screen.blit(self.J,(605,300))
        self.screen.blit(self.K,(605,350))
        self.screen.blit(self.L,(605,400))
        self.screen.blit(self.Spacebar,(605,452.5))
        self.screen.blit(self.gear,(605,480))
        self.screen.blit(self.m,(605,525))
        self.screen.blit(self.start,self.startRect)
        if self.startRect.collidepoint(self.mx,self.my):	#handling start/continue button hovering
            self.screen.blit(self.startHover,self.startRect)
    def run(self):		#game loop function
        self.done = False
        while not self.done:
            self.mx,self.my = mouse.get_pos()
            for e in event.get():
                if e.type==QUIT:
                    self.done = True
                if e.type==MOUSEBUTTONUP and self.startRect.collidepoint(self.mx,self.my):		#if the start button is pressed
                        self.done = True
                        from Menu import menu
                        menu()		#go back to the main game
            self.screen.blit(self.instructionsBG,(0,0))		#blit the instructions background
            self.instructions()		#blit all of the images and text
            display.flip()
        quit()
