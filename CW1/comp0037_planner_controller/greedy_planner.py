# -*- coding: utf-8 -*-

from cell_based_forward_search import CellBasedForwardSearch
from collections import deque



class GREEDYPlanner(CellBasedForwardSearch):

    # Construct the new planner object
    def __init__(self, title, occupancyGrid):
        CellBasedForwardSearch.__init__(self, title, occupancyGrid)
        self.greedyQueue = dict()
		
    def getLength(self):
	return len(self.greedyQueue)
    # Simply put on the end of the queue and then sort the queue by the cost
    def pushCellOntoQueue(self, cell):
        cost = self.computeLStageAdditiveCost(self.goal, cell)
        self.greedyQueue[cell] = cost

    # Check the queue size is zero
    def isQueueEmpty(self):
        return not self.greedyQueue

    # Simply pull from the front of the list
    def popCellFromQueue(self):
        cell = min(self.greedyQueue,key=self.greedyQueue.get)
        del self.greedyQueue[cell]
        return cell

    def resolveDuplicate(self, cell, parentCell):
        # Nothing to do in self case
        pass

