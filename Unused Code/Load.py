import pickle as p
import os

class game():   #placeholder for actual game class
    def __init__(self):
        self.vars = True #where all the initial variables/booleans/etc. go
    def load(self):
        if os.path.isfile("savedat"):
            if os.stat("savedat").st_size!=0:
                self.savedat = p.load(open("savedat","rb"))
                self.hearts,self.pos,self.rupeenum,self.arrowtot,self.bombtot = self.savedat["curhearts"],self.savedat["curpos"],self.savedat["currupee"],self.savedat["curarrow"],self.savedat["curbomb"]
                print(gm.hearts,gm.pos,gm.rupeenum,gm.arrowtot,gm.bombtot)
        else:
            print("No Save Data")
gm = game()
if __name__=="__main__":
    gm.load()
