from pygame import *
from imageload import imageload
from Instructions import Instructions
from Credits import Credits
import pickle
import sys
#Setting the window position
import os
def menu():
  
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10,30"
    screen = display.set_mode((800,740))
    screenx,screeny = screen.get_size()     #set so only display window res needs to be changed
    done = False
    #Menu Stuff
    play = False    #What determines when to start the game
    #Music
    mixer.init()
    confirm = mixer.Sound("music/VideogameConfirmationEDIT.flac")
    mixer.music.load("music/menumusic.mp3")
    mixer.music.set_volume(0.015)   #Can change later, but anything past 0.03 seems really loud
    mixer.music.play()
    #Images
    menuBG = image.load("images/titlescreen/menuBG.png")
    menuBG = transform.scale(menuBG,(screenx,screeny))  #Always fits screen
    #Rect for recognizing Play button -- change this if window size changes
    menuPlay = Rect(335,640,131,70)
    #Hovering play button image
    menuHover = imageload("images/titlescreen/menuHover.png")
    menuHover = transform.scale(menuHover,(131,70))
    #Regular exit image
    menuExit = imageload("images/titlescreen/menuExit.png")
    menuExit = transform.scale(menuExit,(130,55))
    menuExitRect = Rect(10,5,115,45)#can't use menuExit.get_rect() -- the image itself has extra space
    #Hovering exit image
    menuExitHover = imageload("images/titlescreen/menuExitHover.png")
    menuExitHover = transform.scale(menuExitHover,(130,55))

    creditsbutton = imageload("images/titlescreen/Credits.png")
    creditsRect = creditsbutton.get_rect()
    creditsRect.center = (screen.get_rect().right-65,30)
    creditsHover = imageload("images/titlescreen/CreditsHover.png")

    restartbutton = imageload("images/titlescreen/Restart.png")
    restartRect = restartbutton.get_rect()
    restartRect.center = (screen.get_rect().centerx,30)
    restartHover = imageload("images/titlescreen/RestartHover.png")

    controlsbutton = imageload("images/titlescreen/ControlsHover.png")
    controlsRect = controlsbutton.get_rect()
    controlsRect.center = (screen.get_rect().centerx,100)
    controlsHover = imageload("images/titlescreen/Controls.png")

    instructions = Instructions()
    Credits_ = Credits()
    #MenuLoop
    while not done:
        for e in event.get():
            if e.type==QUIT:
                done = True
        mb = mouse.get_pressed()
        mx,my = mouse.get_pos()
        #before play is pressed:
        if not play:
            screen.blit(menuBG,(0,0))   #Background + regular play button
            screen.blit(menuExit,(0,0)) #Exit button
            screen.blit(creditsbutton,(creditsRect))
            screen.blit(controlsbutton,(controlsRect))
            screen.blit(restartbutton,(restartRect))
            if menuPlay.collidepoint(mx,my):    #if mouse is on play button,
                screen.blit(menuHover,(335,640))#blit hover pic
                if mb[0]==1:    #if we click play
                    play = True
                   
            if creditsRect.collidepoint(mx,my):
                screen.blit(creditsHover,(creditsRect))
                if mb[0]==1:
                    Credits_.run()
            if controlsRect.collidepoint(mx,my):
                screen.blit(controlsHover,(controlsRect))
                if mb[0]==1:
                    instructions.instructions()
                    instructions.run()
            if restartRect.collidepoint(mx,my):
                screen.blit(restartHover,(restartRect))
                if mb[0]==1:
                    confirm.play()
                    savedat = {"hearts":10,"bkeys":0,"posx":300,"posy":200,"location":(-1,0),"rupee":30
                               ,"arrow":10,"bomb":10,"hasmap":False,"fairy":0,
                               "keysleft":[[250,250,(-1,0)],[518,502,(5,1)],[369,239,(7,4)],[454,119,(0,2)],[310,688,(1,0)]
                                           ,[624,200,(1,2)],[505,695,(4,2)],[415,126,(9,5)]]}
       
                   
                    open("savedat","w").close()
##                if os.stat("savedat").st_size==0:
                    pickle.dump(savedat,open("savedat","wb"))
                    
                    
            if menuExitRect.collidepoint(mx,my):    #if mouse is on exit button
                screen.blit(menuExitHover,(0,0))    #blit exithover pic
                if mb[0]==1:    #if we want to exit the game
                    done = True
            
        else:       #Starts the main game loop and closes the menu window
##            mixer.music.stop() #Stops music -- may run into music conflict later on with game file, if conflict occurs it can be fixed by putting the music files in a queue
##            #assumes that the main game loop is called game.py
##            #if it ends up being main.py or something else we can always change this
            
            done = True
        if play:
            done=True
            
            
            
        display.flip()
    if play==True:
       
        import link6
    else:
        quit()
if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
    menu()
##   link3()
