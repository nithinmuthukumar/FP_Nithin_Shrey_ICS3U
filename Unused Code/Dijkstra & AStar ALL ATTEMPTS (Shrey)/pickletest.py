import json, gridinit

grid7 = [
        [1,3,3,3,3,3,3,3,3,3],
        [3,3,3,3,3,3,3,3,3,3],
        [3,3,3,3,3,3,3,3,3,3],
        [3,3,3,3,3,3,3,3,3,3],
        [3,3,3,3,3,3,3,3,3,3],
        [3,3,3,3,3,3,3,3,3,3],
        [3,3,3,3,3,3,3,3,3,3],
        [3,3,3,3,3,3,3,3,3,3],
        [3,3,3,3,3,3,3,3,3,3],
        [3,3,3,3,3,3,3,3,3,2]
        ]

grid7todict = gridinit.gridtodict(grid7)
start = list(grid7todict.keys())[0]
end = list(grid7todict.keys())[-1]
print(gridinit.get_shortest_path(grid7todict,start,end))
##print(start,end)
##print(grid7todict.get(start))
##print(grid7todict.get('(0, 0)'))

##with open('mapdict.txt', 'w') as file:
##    file.write(json.dumps(str(grid7todict)))    #write mode changed from w to wb as w raises TypeError


##class add():    #lets me add additional duplicate keys
##    def __init__(self,name):
##      self.name = name
##    def __repr__(self):
##        return self.name
##alternate = {}
##for i in range(10):
##    alternate[add("Andy")] = i
###alternate = {person("Andrew") : "Cambridge", person("Barabara") : "Bloomsbury", person("Andrew"): "Corsica"}
##print(alternate)
