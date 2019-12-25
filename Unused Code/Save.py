import pickle as p
import os

class game():   #placeholder for actual game class
    def __init__(self):
        self.hearts = 3
        self.pos = (20,20)
        self.rupeenum = 150
        self.arrowtot = 5
        self.bombtot = 2
        self.hasmap=False
##Make sure this boolean is included in main program
##"""Just copy/past everything below this string"""
    def save(self):
        self.savedat = {"hearts":3,"bkeys":0,"posx":200,"posy":200,"location":(-1,0),"rupee":30,"arrow":0,"bomb":0,"hasmap":False,"fairy":0}
       
        if not os.path.isfile("savedat"):
                p.dump(self.savedat,open("savedat","wb"))
                self.saved = True
        else:
            open("savedat","w").close()
##                if os.stat("savedat").st_size==0:
            p.dump(self.savedat,open("savedat","wb"))
gm = game()
if __name__=="__main__":
    gm.save()
