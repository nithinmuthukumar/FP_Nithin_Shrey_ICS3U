array = []
for x in range(500):
    x = []
    for y in range(500):
        x.append(1)
    array.append([x])

file = open('2dmap.txt','w')
file.write(str(array))
