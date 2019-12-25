from pygame import *
from imageload import imageload
from GameWinScrollClass import scroll
from random import randint
import os 
os.environ['SDL_VIDEO_CENTERED'] = '1'
font.init()
screen = display.set_mode((800,740))
timer = 0
medfont = font.Font("ReturnOfGanon.ttf", 75)
GameWinTitleColor = (200,255,0)
GameWinTitle = medfont.render("You Win!", 0, GameWinTitleColor)
GameWinTitleRect = GameWinTitle.get_rect()
GameWinTitleRect.center = screen.get_rect().centerx,75
GameWinBG = imageload("images/GameWin/GameWinBG.png",1,False,(255,255,255))
GameWinBGRect = GameWinBG.get_rect()
GameWinBGRect.center = screen.get_rect().center
Exit = imageload("images/GameOver/Exit.png",0.5,False,(255,255,255))
ExitRect = Exit.get_rect()
ExitRect.center = screen.get_rect().centerx,700
ExitHover = imageload("images/GameOver/ExitHover.png",0.5,False,(255,255,255))
EndingText = open("EndingText.txt").read().strip().split("\n")
Ending = scroll(screen,EndingText,(200,255,0))
done = False
clock = time.Clock()
while not done:
    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()
    for e in event.get():
        if e.type==QUIT:
            done = True
        if e.type==MOUSEBUTTONUP:
            if ExitRect.collidepoint(mx,my):
                done = True
    screen.blit(GameWinBG,GameWinBGRect)
    milliseconds = clock.tick(60)
    Ending.offset -= milliseconds / 25 #vertmovement -- decrease to go faster
    if timer < 255:
        timer += 7.5
        TextSurface = GameWinTitle.convert(screen)
        TextSurface.set_alpha(timer)
    else:
        """
        Comment out the next three lines if you don't want title to flash
        """
        GameWinTitleColor = (randint(0,255),randint(0,255),randint(0,255))
        GameWinTitle = medfont.render("You Win!", 0, GameWinTitleColor)
        TextSurface = GameWinTitle.convert(screen)
        if Ending.offset * -1 > Ending.text_height:
            screen.blit(Exit,ExitRect)
        else:
            Ending.run()
        if ExitRect.collidepoint(mx,my):
            screen.blit(ExitHover,ExitRect)
    screen.blit(TextSurface, GameWinTitleRect)
    display.flip()
quit()
