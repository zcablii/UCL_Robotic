# -*- coding: utf-8 -*-

from cell_based_forward_search import CellBasedForwardSearch
from collections import deque
from cell import CellLabel


class DIJKSTRAPlanner(CellBasedForwardSearch):

    def __init__(self, title, occupancyGrid):
        CellBasedForwardSearch.__init__(self, title, occupancyGrid)
        self.dijkstraQueue = dict()

    # Put the cell's path cost into the dictionary
    def pushCellOntoQueue(self, cell):
        if cell.parent:
            cell.pathCost = cell.parent.pathCost+self.computeLStageAdditiveCost(cell.parent, cell)
        self.dijkstraQueue[cell] = cell.pathCost

    # Check the queue size is zero
    def isQueueEmpty(self):
        return not self.dijkstraQueue

    # Simply pull from the front of the list
    def popCellFromQueue(self):
        cell = min(self.dijkstraQueue,key=self.dijkstraQueue.get)
        del self.dijkstraQueue[cell]
        return cell

    def resolveDuplicate(self, cell, parentCell):
        distance = parent.pathCost+self.computeLStageAdditiveCost(cell.parent, cell)
	        if distance < cell.pathCost:
		        cell.pathCost = distance
		        cell.parent = parent
		        self.dijkstraQueue[cell] = cell.pathCost
        pass
