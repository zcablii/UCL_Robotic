# -*- coding: utf-8 -*-

from cell_based_forward_search import CellBasedForwardSearch
from collections import deque
from cell import CellLabel

class AEUCLIDEANPlanner(CellBasedForwardSearch):

    def __init__(self, title, occupancyGrid):
        CellBasedForwardSearch.__init__(self, title, occupancyGrid)
        self.aQueue = dict()

    # Put the cell's path cost and estimated cost to goal into the dictionary
    def pushCellOntoQueue(self, cell):
        if cell.parent:
            cell.pathCost = cell.parent.pathCost+self.computeLStageAdditiveCost(cell.parent, cell)
        self.aQueue[cell] = cell.pathCost + self.computeLStageAdditiveCost(self.goal, cell)

    # Check the queue size is zero
    def isQueueEmpty(self):
        return not self.aQueue

    # Find the cell with the smallest path cost, return it and delete it from the dictionary.
    def popCellFromQueue(self):
        cell = min(self.aQueue,key=self.aQueue.get)
        del self.aQueue[cell]
        return cell
    
    # Resolve Duplicate 
    def resolveDuplicate(self, cell, parent):
        if cell.label != CellLabel.DEAD:
	        distance = parent.pathCost+self.computeLStageAdditiveCost(cell.parent, cell)
	        if distance < cell.pathCost:
		        cell.pathCost = distance
		        cell.parent = parent
		        self.aQueue[cell] = cell.pathCost + self.computeLStageAdditiveCost(self.goal, cell)
        pass
