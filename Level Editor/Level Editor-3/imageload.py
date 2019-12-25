from pygame import*
def imageload(fileadd,size,islist,colorkey=(0,136,255)):#,need to include colorkey for convert
    if islist==True:
        sprites=[]
        for i in fileadd:
            img=image.load(i).convert()
            img.set_colorkey(colorkey)
      
            sprites.append(transform.scale(img,(round(img.get_width()*size),round(img.get_height()*size))))
        return sprites
    else:
        img=image.load(fileadd)
        return transform.scale(img,(round(img.get_width()*size),round(img.get_height()*size)))
