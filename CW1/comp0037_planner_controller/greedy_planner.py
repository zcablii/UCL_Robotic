# -*- coding: utf-8 -*-

from cell_based_forward_search import CellBasedForwardSearch
from collections import deque



class GREEDYPlanner(CellBasedForwardSearch):

    # Construct the new planner object
    def __init__(self, title, occupancyGrid):
        CellBasedForwardSearch.__init__(self, title, occupancyGrid)
        self.greedyQueue = []
        self.costList = []
    def getLength(self):
	return len(self.greedyQueue)
    # Simply put on the end of the queue and then sort the queue by the cost
    def pushCellOntoQueue(self, cell):
        self.greedyQueue.append(cell)
        cost = self.computeLStageAdditiveCost(self.goal, cell)
        self.costList.append(cost)

        ziped_list = zip(self.costList,self.greedyQueue)
        ziped_list.sort()
        self.greedyQueue = [x for _,x in ziped_list]
        self.costList = [x for x,_ in ziped_list]
    # Check the queue size is zero
    def isQueueEmpty(self):
        return not self.greedyQueue

    # Simply pull from the front of the list
    def popCellFromQueue(self):
        cell = self.greedyQueue.pop(0)
        cost = self.costList.pop(0)
        return cell

    def resolveDuplicate(self, cell, parentCell):
        # Nothing to do in self case
        pass

    def costFun(self, cell):
        return self.computeLStageAdditiveCost(self.goal, cell)
