from pygame import *
from imageload import imageload
#"""
#Will not run (need to set up it's own screen), only used to import to other files.
#Class that creates a shop and keeps track of the items bought, the items held before buying, the stock of items remaining, and how much each item costs (+ total cost)
#"""
class shopclass():
    def __init__(self,screen):
        font.init()		#initializing font
 #       """
 #		creates all images, and sets their position before the game loop.
 #		hyliantot = displays of how many rupees the player currently has
 #		hylian = displays of how much of one item/weapon the player is buying
 	#	rupeenum = current number of rupees the player has
 	#	hasmap = whether the player has purchased the map or not
 	#	ui = the subsurface onto which the shop is blitted
 	##	weapons = the "weapons" tab shop items
 	#	items = the "items" tab shop items
 	#	tab = the tab that is changed when clicked on, that is used to signify that you're viewing the item tab or the weapon tab
 	#	ExitHover = the shop exit button hover image
 	#	buyhover = the shop buy button hover image
 	#	sellhover = the shop sell button hover image
 	#	"""
        self.hyliantot,self.hylian = font.Font('ReturnofGanon.ttf', 35),font.Font('ReturnofGanon.ttf', 20)
        self.rupeenum,self.hasmap = 0,False
        self.ui = screen.subsurface(screen.get_rect())
        self.weapons = imageload("images/shop/shop1Improved2.png",1,False,(255,255,255))
        self.weaponsRect = self.weapons.get_rect()
        self.weaponsRect.center = (self.ui.get_rect().center[0],self.ui.get_rect().center[1]+((800-screen.get_rect().bottom)//2))
        self.items = imageload("images/shop/shop2.png",1,False,(255,255,255))
        self.tab = imageload("images/shop/itemtab.png",1,False,(255,255,255))
        self.toggleTabRect = self.tab.get_rect()
        self.toggleTabRect.center = self.weaponsRect.center[0],self.weaponsRect.center[1]-45
        self.ExitHover = imageload("images/shop/ExitHover.png",1,False,(255,255,255))
        self.ExitRect = self.ExitHover.get_rect()
        self.ExitRect.topright = self.weaponsRect.topright[0]-8,self.weaponsRect.topright[1]+7
        self.buyhover = imageload("images/shop/BuyHover.png",1,False,(255,255,255))
        self.sellhover = imageload("images/shop/SellHover.png",1,False,(255,255,255))
      
        self.tabbool = 1	#shows which tab the player is currently on -- "item", or "weapon"
 #       """
 #       ...Left,
 #       ...Right
 #      rectangles are the arrows that are used to determine if the player adds or subtracts from the shop stock / their own temporary inventory
 #       """
        self.BombLeft = Rect(351,400,9,13)
        self.BombRight = Rect(388,400,9,13)
        self.SwordLeft = Rect(435,400,9,13)
        self.SwordRight = Rect(471,400,9,13)
        self.ArrowLeft = Rect(351,448,9,13)
        self.ArrowRight = Rect(388,448,9,13)
        self.Qs = [self.BombLeft,self.BombRight,self.SwordLeft,self.SwordRight,self.ArrowLeft,self.ArrowRight]		#all the weapon arrowheads in a list
 #       """
 #       QVals = how much each weapon is worth (there is a repeat for each because they can be added/subtracted -- I figured out how to cut this down by the time I finished the "item" tab)
	#	QStock = the current stock of the weapons that the shop has
	#	QMaxStock = the 'ideal'/ beginning stock of each weapon -- used to make sure you can't give back more weapons to the stock than there were originally
	#	held = how much of each weapon inventory the player currently temporarily has (before they press buy)
 #       ""
 #bkey 2 map 
        self.QVals,self.QStock,self.QMaxStock,self.held = [15,15,75,75,5,5],[float("inf"),float("inf"),1,1,float("inf"),float("inf")],[float("inf"),float("inf"),1,1,float("inf"),float("inf")],[0,0,0,0]
        self.HeartLeft = Rect(337,401,9,13)
        self.HeartRight = Rect(374,401,9,13)
        self.FairyLeft = Rect(421,400,9,13)
        self.FairyRight = Rect(457,400,9,13)
        self.MapLeft = Rect(337,448,9,13)
        self.MapRight = Rect(374,448,9,13)
        self.KeyLeft = Rect(421,448,9,13)
        self.KeyRight = Rect(457,448,9,13)
        self.itemQs,self.itemQVals,self.itemQStock,self.itemQMaxStock,self.itemheld = [self.HeartLeft,self.HeartRight,self.FairyLeft,self.FairyRight,self.MapLeft,self.MapRight,self.KeyLeft,self.KeyRight],[50,50,25,25,20,20,50,50],[12,12,5,5,1,1,1,1],[12,12,5,5,1,1,1,1],[0,0,0,0]
        self.buyrect = Rect(401,469,75,25)
        self.sellrect = Rect(321,469,75,25)
        self.cost = 0	#cost is how much the total amount of weapons/items will cost
 #       """
 #       amt 0 through amt 7 is text that displays how much of the current stock of their respective item/weapon the player will be buying up
 #       """
        self.amt0,self.amt1,self.amt2,self.amt4,self.amt5,self.amt6,self.amt7 = self.hylian.render('0',False,(173,214,198)),self.hylian.render('0',False,(173,214,198)),self.hylian.render('0',False,(173,214,198)),self.hylian.render('0',False,(173,214,198)),self.hylian.render('0',False,(173,214,198)),self.hylian.render('0',False,(173,214,198)),self.hylian.render('0',False,(173,214,198))
        self.amt0rect,self.amt1rect,self.amt2rect,self.amt4rect,self.amt5rect,self.amt6rect,self.amt7rect = self.amt0.get_rect(),self.amt1.get_rect(),self.amt2.get_rect(),self.amt4.get_rect(),self.amt5.get_rect(),self.amt6.get_rect(),self.amt7.get_rect()
        self.amt0rect.center,self.amt1rect.center,self.amt2rect.center,self.amt4rect.center,self.amt5rect.center,self.amt6rect.center,self.amt7rect.center = (375,408),(458,408),(375,455),(360,408),(443,408),(360,456),(443,456)
 #       """
 #       dictionary generated for ease of referring to each text -- 0 instead of amt0, 1 instead of amt1
 #       used in the main loop when decided which amt to update
 #       """
        self.amt = {0:self.amt0,1:self.amt1,2:self.amt2,4:self.amt4,5:self.amt5,6:self.amt6,7:self.amt7}
        self.hearts=0	#how many hearts the player currently has
        self.bombtot=0	#how many bombs the player currently has
        self.Fairies=0	#how many fairies the player currently has
        self.arrowtot=0	#how many arrows the player currently has
        self.Keys=0		#how many keys the player currently has
        self.rupeepic = imageload("images/UI/rupee.png",0.175,False,(255,255,255))		#rupee image blitted next to rupeenum
    
        self.rupeecolon = self.hylian.render(":",False,(205,255,0))						#colon blitted between rupeepic and rupeenum
        
    def rupeehandling(self,rupeenum):
 #   	"""
 #   	keeps track of and blits the current amount of rupees the player has.
 #  	"""
        self.ui.blit(self.rupeepic,(self.rupeepic.get_rect(x=0,y=25)))
        
        self.rupeenum=rupeenum
        self.rupees = self.hyliantot.render('%i'% self.rupeenum,False,(205,255,0))
        self.ui.blit(self.rupees,(35,25))
    def shop(self,mx,my):
 	#	"""
 	#	blits the actual shop, and blits the tab that is used to toggle between tabs,
 	#	allows for the blitting of the "item" tab, blits the exit, buy and sell button,
 	#	while also handling their respective hover images
 	#	"""
        
        self.ui.blit(self.weapons,self.weaponsRect)
        if self.tabbool==-1:
            self.ui.blit(self.tab,self.toggleTabRect)
            self.ui.blit(self.items,self.weaponsRect)
        if self.buyrect.collidepoint(mx,my):
            self.ui.blit(self.buyhover,self.buyrect)
        if self.sellrect.collidepoint(mx,my):
            self.ui.blit(self.sellhover,self.sellrect)
        if self.ExitRect.collidepoint(mx,my):
            self.ui.blit(self.ExitHover,self.ExitRect)
    def loop(self):
        done = False
        clock = time.Clock()
        while not done:
            mx,my = mouse.get_pos()
            mb = mouse.get_pressed()
            for e in event.get():
                if e.type==QUIT:
                    done = True
                if e.type==MOUSEBUTTONUP:
                    
                    if self.ExitRect.collidepoint(mx,my):		#close the menu if exit button is clicked
                            done=True
                    if self.tabbool==1:		#deals with "weapon" tab
                        for q in range(len(self.Qs)):	#looks at all of the arrows on the weapon tab
                            if self.Qs[q].collidepoint(mx,my):	#if the current arrow is clicked by the player
                            	#if it's an "add stock" arrow and the player can afford it's price and it's still in stock (checked two different ways):
                                if q%2!=0 and self.cost+self.QVals[q]<=self.rupeenum and self.QStock[q] and self.held[q//2]+1<=self.QStock[q]:
                                    self.cost+=self.QVals[q]	#add the weapon's price to the total cost
                                    self.QStock[q]-=1			#take one out of the stock for that weapon
                                    self.OldQStock = q			#keeps track of the button pressed in case the player wants to subtract that same item again
                                    self.held[q//2]+=1			#increases the players temporary stock
                                    self.amt[q//2] = self.hylian.render('%i'% self.held[q//2],False,(173,214,198))		#visibly shows the number of stock for that weapon that the player will be buying
                                #if it's a "subtract stock" arrow and the amount will not be negative and the player actually has it in stock
                                elif q%2==0 and self.cost-self.QVals[q]<=self.rupeenum and self.cost-self.QVals[q]>=0 and self.held[q//2]-1>=0:
                                    self.cost-=self.QVals[q]	#removes it from total cost
                                    self.QStock[self.OldQStock]+=1	#adds it to the shop's previous stock
                                    self.held[q//2]-=1			#removes it from player's current temporary stock
                                    self.amt[q//2] = self.hylian.render('%i'% self.held[q//2],False,(173,214,198))		#visibly shows the decrease in the number of items the player will be buying
                                print("Current Cost: $",self.cost)
                                print("Stocks:",self.held)
                    # this is the exact same thing as the earlier block of code, but it uses its own variables to keep track of all costs/stocks/etc. of it's own tab
                    if self.tabbool==-1:
                        for q in range(len(self.itemQs)):
                            if self.itemQs[q].collidepoint(mx,my):
                                if q%2!=0 and self.cost+self.itemQVals[q]<=self.rupeenum and self.itemQStock[q] and self.itemheld[q//2]+1<=self.itemQStock[q]:
                                    self.cost+=self.itemQVals[q]
                                    self.itemQStock[q]-=1
                                    self.itemOldQStock = q
                                    self.itemheld[q//2]+=1
                                    self.amt[4+q//2] = self.hylian.render('%i'% self.itemheld[q//2],False,(173,214,198))
                                elif q%2==0 and self.cost-self.itemQVals[q]<=self.rupeenum and self.cost-self.itemQVals[q]>=0 and self.itemheld[q//2]-1>=0:
                                    self.cost-=self.itemQVals[q]
                                    self.itemQStock[self.itemOldQStock]+=1
                                    self.itemheld[q//2]-=1
                                    self.amt[4+q//2] = self.hylian.render('%i'% self.itemheld[q//2],False,(173,214,198))
                                print("Current Cost: $",self.cost)
                                print("Stocks:",self.held)
             		#if the player tries to buy the items he added:
                    if self.buyrect.collidepoint(mx,my) and self.cost<=self.rupeenum and self.cost!=0:
                        self.rupeenum-=self.cost	#subtract the cost from the number of rupees the player has
 #                       """
 #                       adds all of the items that the player bought
 #                       i.e. adds the hearts, fairies, keys, bombs and arrows bought
 #                       sets hasmap to true if map was purchased                    
 #                       """
                        if self.amt[4] and self.itemheld[0]:
                            self.hearts+=self.itemheld[0]
                        if self.amt[5] and self.amt[5] and self.itemheld[1]:
                            self.Fairies+=self.itemheld[1]
                        if self.amt[6] and self.amt[6] and self.itemheld[2]:
                            self.hasmap = True
                        if self.amt[7] and self.amt[7] and self.itemheld[3]:
                            self.Keys+=self.itemheld[3]
                        self.bombtot+=self.held[0]
                        self.arrowtot+=self.held[2]
 #                       """
 #                       Resets amt dictionary to it's intial state
 #                       Resets the stock of weapons/items held
 #                      Resets the cost to 0
 #                       """
                        self.amt[0],self.amt[1],self.amt[2],self.amt[4],self.amt[5],self.amt[6],self.amt[7] = self.amt0,self.amt1,self.amt2,self.amt4,self.amt5,self.amt6,self.amt7
                        print("Spent $",self.cost)
                        self.held,self.itemheld,self.cost = [0,0,0,0],[0,0,0,0],0
                    if self.toggleTabRect.collidepoint(mx,my):	#if the tab is pressed
                        self.tabbool*=-1
            self.shop(mx,my)	#blits the shop
            if self.tabbool==1:		#displays the number of weapons the player will buy for each weapon
                self.ui.blit(self.amt[0],self.amt0rect)
                self.ui.blit(self.amt[1],self.amt1rect)
                self.ui.blit(self.amt[2],self.amt2rect)
            else:		#displays the number of items the player will buy for each item
                self.ui.blit(self.amt[4],self.amt4rect)
                self.ui.blit(self.amt[5],self.amt5rect)
                self.ui.blit(self.amt[6],self.amt6rect)
                self.ui.blit(self.amt[7],self.amt7rect)
            clock.tick(60)
            display.flip()
            print(self.itemQStock,self.itemQMaxStock)
      	#return all changed values that matter to the main game, so that new items can be recieved and used/made a part of the main game
        return self.hearts,self.bombtot,self.arrowtot,self.Fairies,self.hasmap,self.Keys,self.rupeenum
        
                
  
if __name__=="__main__":
    loop()
