import rospy
from math import *
from explorer_node_base import ExplorerNodeBase

# This class implements a super dumb explorer. It goes through the
# current map and marks the first cell it sees as the one to go for

class ExplorerNodeLargestFrontier(ExplorerNodeBase):

    def __init__(self):
        ExplorerNodeBase.__init__(self)
        
        self.blackList = []
        self.position = (0,0)
   

    def calculateDistance(self,p1, p2):
        width = p2[0] - p1[0]
        height = p2[1] - p2[1]
        return sqrt(width**2+height**2)

    def isAdjacent(self,point1, point2):
        if((point1[0]+1==point2[0] and point1[1]==point2[1])|(point1[0]-1==point2[0] and point1[1]==point2[1])|(point1[0]==point2[0] and point1[1]+1==point2[1])|
        (point1[0]==point2[0] and point1[1]-1==point2[1])|(point1[0]+1==point2[0] and point1[1]+1==point2[1])|(point1[0]+1==point2[0] and point1[1]-1==point2[1])|
        (point1[0]-1==point2[0] and point1[1]+1==point2[1])|(point1[0]-1==point2[0] and point1[1]-1==point2[1])):
            return True
        else:
            return False
            
    def AllNeighbour(self, point, frontierList):
        result = []
        result.append(point)
        for i in range(-, len(frontierList)-1):
            if(self.isAdjacent(point,frontierList[i])):
                result.extend(self.AllNeighbour(frontierList[i], frontierList))
        return result

    def largestFrontier(self, frontierList):
        largest = []
        while(len(frontierList) is not 0):
            point = frontierList.pop(0)
            self.AllNeighbour(point, frontierList)
            

    def isAdjacent(self,point1, point2):
        if((point1[0]+1==point2[0] and point1[1]==point2[1])|(point1[0]-1==point2[0] and point1[1]==point2[1])|(point1[0]==point2[0] and point1[1]+1==point2[1])|
        (point1[0]==point2[0] and point1[1]-1==point2[1])|(point1[0]+1==point2[0] and point1[1]+1==point2[1])|(point1[0]+1==point2[0] and point1[1]-1==point2[1])|
        (point1[0]-1==point2[0] and point1[1]+1==point2[1])|(point1[0]-1==point2[0] and point1[1]-1==point2[1])):
            return True
        else:
            return False
            


    def pushToList(self,point, List):
   
        for group in List:
            for gpoint in group:
                if(self.isAdjacent(point,gpoint)):
                    group.append(point)
                    return List
        return List.append([point])      
    def largestFrontier(self, frontierList):
        sortList = []
        while(len(list) is not 0):
            point = list.pop(0)
            print(point)
    
            if(len(sortList)==0):
                sortList.append([point])
                print(sortList)     
                continue
            pushToList(point, sortList)
        max = 0
        maxGroup = []
        for group in sortList:
            if len(group)>max:
                max = len(group)
                maxGroup = group
        return maxGroup
    def chooseNewDestination(self):


#         print 'blackList:'
#         for coords in self.blackList:
#             print str(coords)
        
        candidateGood = False
        destination = None
        smallestD2 = float('inf')

        for point in self.frontierList:
                candidate = (point[0], point[1])
                
                    
                candidateGood = True
                for k in range(0, len(self.blackList)):
                    if self.blackList[k] == candidate:
                        candidateGood = False
                        break
                    
                if candidateGood is True:
                    d2 = self.calculateDistance(self.position, candidate)

                    if (d2 < smallestD2):
                        candidateGood = False
                        destination = candidate
                        smallestD2 = d2
        
        return candidateGood, destination
        # If we got a good candidate, use it

        

    def destinationReached(self, goal, goalReached):
        if goalReached is False:
#             print 'Adding ' + str(goal) + ' to the naughty step'
            self.blackList.append(goal)
        else:
            self.position = goal
            
