from pygame import*
def imageload(fileadd,size=1,islist=False,colorkey=(0,0,0)):#,need to include colorkey for convert
    if islist==True:
        sprites=[]
        for i in fileadd:
            img=image.load(i).convert_alpha()
            img.set_colorkey((0,0,0))
      
            sprites.append(transform.scale(img,(round(img.get_width()*size),round(img.get_height()*size))))
        return sprites
    else:
        img=image.load(fileadd)
        return transform.scale(img,(round(img.get_width()*size),round(img.get_height()*size)))
