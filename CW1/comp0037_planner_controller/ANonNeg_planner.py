# -*- coding: utf-8 -*-

from cell_based_forward_search import CellBasedForwardSearch
from collections import deque
from cell import CellLabel

# This class implements the FIFO - or breadth first search - planning
# algorithm. It works by using a double ended queue: cells are pushed
# onto the back of the queue, and are popped from the front of the
# queue.

class ASTARNONNEGPlanner(CellBasedForwardSearch):

    # self implements an A* search algorithm
    
    def __init__(self, title, occupancyGrid):
        CellBasedForwardSearch.__init__(self, title, occupancyGrid)
        self.aQueue = dict()

    # Put the cell's estimated cost into the dictionary
    def pushCellOntoQueue(self, cell):
        if cell.parent:
            cell.pathCost = cell.parent.pathCost+self.computeLStageAdditiveCost(cell.parent, cell)
        self.aQueue[cell] = cell.pathCost + 5

	
    # Check the queue size is zero
    def isQueueEmpty(self):
        return not self.aQueue

    # Pop the cell with the smallest path cost
    def popCellFromQueue(self):
        cell = min(self.aQueue,key=self.aQueue.get)
        del self.aQueue[cell]
        return cell
    
    # resolve Duplicate
    def resolveDuplicate(self, cell, parent):
        if cell.label != CellLabel.DEAD:
	        distance = parent.pathCost+self.computeLStageAdditiveCost(cell.parent, cell)
	        if distance < cell.pathCost:
		        cell.pathCost = distance
		        cell.parent = parent
		        self.aQueue[cell] = cell.pathCost + 5
        pass
