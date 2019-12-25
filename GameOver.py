from pygame import *
from imageload import imageload
import os
from Menu import menu
os.environ['SDL_VIDEO_CENTERED'] = '1'	#centers the window
font.init()	#initalizing font
screen = display.set_mode((800,740))	#intializing display
timer = 0	#used to calculate the alpha value of the title (so the title can fade in), as well as when to stop changing the alpha value of the title.
medfont = font.Font("ReturnOfGanon.ttf", 75)	#big font used for all text in this file
GameOverText = medfont.render("Game Over", 0, (255,0,0))	#"game over" text that fades into view
GameOverTextRect = GameOverText.get_rect()
GameOverTextRect.center = screen.get_rect().centerx,75		#sets the "game over" text position before game loop
GameOverBG = imageload("images/GameOver/GameOverBG.png",1,False,(255,255,255))	#the background of the game over screen
Exit = imageload("images/GameOver/Exit.png",0.5,False,(255,255,255))	#exit button -- closes the game
ExitRect = Exit.get_rect()
ExitRect.center = 150,400		#setting exit button position before game loop
ExitHover = imageload("images/GameOver/ExitHover.png",0.5,False,(255,255,255))
Continue = imageload("images/GameOver/Continue.png",0.5,False,(255,255,255))	#continue button -- returns user back to main menu
ContinueRect = Continue.get_rect()
ContinueRect.center = 600,400	#setting continue button position before game loop
ContinueHover = imageload("images/GameOver/ContinueHover.png",0.5,False,(255,255,255))

done = False
while not done:
    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()
    for e in event.get():
        if e.type==QUIT:
            done = True
        if e.type==MOUSEBUTTONUP:
            if ExitRect.collidepoint(mx,my):	#if the user wants to quit the game
                done = True
            if ContinueRect.collidepoint(mx,my):	#if the user wants to keep on playing
                menu()
    screen.blit(GameOverBG,(0,0))	#blits game over screen background
    if timer < 255:		#if opacity is less than 255 (which is the highest possible opacity)
        timer += 5		#add to the opacity
        TextSurface = GameOverText.convert(screen)	#copies text to a surface
        TextSurface.set_alpha(timer)	#sets the surface alpha value (can't do this with text by itself)
    else:
        screen.blit(Continue,ContinueRect)		#blit the continue button
        screen.blit(Exit,ExitRect)		#blit the exit button
        if ExitRect.collidepoint(mx,my):	#handling hovering for exit button
            screen.blit(ExitHover,ExitRect)
        if ContinueRect.collidepoint(mx,my):	#handling hovering for continue button
            screen.blit(ContinueHover,ContinueRect)
    screen.blit(TextSurface, GameOverTextRect)	#blit the "game over" title
    display.flip()
quit()
