# -*- coding: utf-8 -*-

from cell_based_forward_search import CellBasedForwardSearch
from collections import deque

# This class implements the FIFO - or breadth first search - planning
# algorithm. It works by using a double ended queue: cells are pushed
# onto the back of the queue, and are popped from the front of the
# queue.

class AMANHATTANPlanner(CellBasedForwardSearch):

    # Construct the new planner object
    def __init__(self, title, occupancyGrid):
        CellBasedForwardSearch.__init__(self, title, occupancyGrid)
        self.AStarQueue = []
        self.costList = []

    # Simply put on the end of the queue
    def pushCellOntoQueue(self, cell):
        self.AStarQueue.append(cell)
        if(cell.parent):
            cell.pathCost = cell.parent.pathCost + self.computeLStageAdditiveCost(cell.parent, cell) + self.ManhattanCost(self.goal, cell)
        cost = cell.pathCost
        self.costList.append(cost)

        ziped_list = zip(self.costList,self.AStarQueue)
        ziped_list.sort()
        self.AStarQueue = [x for _,x in ziped_list]
        self.costList = [x for x,_ in ziped_list]

    # Check the queue size is zero
    def isQueueEmpty(self):
        return not self.AStarQueue

    # Simply pull from the front of the list
    def popCellFromQueue(self):
        cell = self.AStarQueue.pop(0)
        cost = self.costList.pop(0)
        return cell

    def resolveDuplicate(self, cell, parentCell):
        predicted_cost = parentCell.pathCost + self.computeLStageAdditiveCost(parentCell, cell) + self.ManhattanCost(self.goal, cell)
        if(cell.pathCost> predicted_cost):
            cell.parent = parentCell
            cell.pathCost = predicted_cost

            ziped_list = zip(self.costList,self.AStarQueue)
            ziped_list.sort()
            self.AStarQueue = [x for _,x in ziped_list]
            self.costList = [x for x,_ in ziped_list]

    def ManhattanCost(self, goal, cell):
        xCost = abs(goal.coords[0]-cell.coords[0])
        yCost = abs(goal.coords[1]-cell.coords[1])
        return xCost + yCost