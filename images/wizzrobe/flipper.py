from pygame import*
from glob import*
def flip(pics,filename):
    for i in range(len(pics)):
        pic=image.load(pics[i])
        flipic=transform.flip(pic,True,False)
        image.save(flipic,filename+str(i)+".png")
flip(glob("wizzroberight/*.png"),"wizzrobeleft")
