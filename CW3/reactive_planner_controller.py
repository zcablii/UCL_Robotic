# This class manages the key logic for the reactive planner and
# controller. This monitors the the robot motion.

import rospy
import threading
import time
from cell import CellLabel
from planner_controller_base import PlannerControllerBase
from comp0037_mapper.msg import *
from comp0037_reactive_planner_controller.aisle import Aisle

class ReactivePlannerController(PlannerControllerBase):

    def __init__(self, occupancyGrid, planner, controller):
        PlannerControllerBase.__init__(self, occupancyGrid, planner, controller)
        
        self.mapUpdateSubscriber = rospy.Subscriber('updated_map', MapUpdate, self.mapUpdateCallback)
        self.gridUpdateLock =  threading.Condition()
        self.aisleToDriveDown = None
        self.time_to_wait = 0
        self.lamda_B = 0.05
        self.P_B = 0.8
        self.alter_aisle_lowestCost = 99999
        self.startPos = (0,0)
    def mapUpdateCallback(self, mapUpdateMessage):

        # Update the occupancy grid and search grid given the latest map update
        self.gridUpdateLock.acquire()
        self.occupancyGrid.updateGridFromVector(mapUpdateMessage.occupancyGrid)
        self.planner.handleChangeToOccupancyGrid()
        self.gridUpdateLock.release()

        # If we are not currently following any route, drop out here.
        if self.currentPlannedPath is None:
            return

        self.checkIfPathCurrentPathIsStillGood()

    def checkIfPathCurrentPathIsStillGood(self):

        # This methods needs to check if the current path, whose
        # waypoints are in self.currentPlannedPath, can still be
        # traversed
                
        # If the route is not viable any more, call
        # self.controller.stopDrivingToCurrentGoal()
        waypoints = self.currentPlannedPath.waypoints
        for waypoint in waypoints:
            dX = waypoint.coords[0]
            dY = waypoint.coords[1]

            if self.occupancyGrid.getCell(dX, dY) == 1:
                self.controller.stopDrivingToCurrentGoal()
                break

    # Choose the first aisle the robot will initially drive down.
    # This is based on the prior.
    def chooseInitialAisle(self, startCellCoords, goalCellCoords):
        L_w = 2
        pathViaB = self.planPathToGoalViaAisle(startCellCoords, goalCellCoords, Aisle.B)
        print("============================")
        print("path cost of " + str(Aisle.B) + " is " + str(pathViaB.travelCost))        
        print("============================")

        pathViaC = self.planPathToGoalViaAisle(startCellCoords, goalCellCoords, Aisle.C)
        print("path cost of " + str(Aisle.C) + " is " + str(pathViaC.travelCost))        
        print("============================")
        threshold = (pathViaC - pathViaB)/(L_w * self.P_B)
        print("threshold =" + str(threshold))
        print("============================")
        
        
        T = 1.0/self.lamda_B
        pathViaB = pathViaB + T * L_w * self.P_B
        lowestCost = 0
        if (pathViaC.travelCost > pathViaB.travelCost):
            #lowestCost = pathViaB.travelCost
            return B
            
        else:
            #lowestCost = pathViaC.travelCost
            return Aisle.C

        #lamda_B  is  self.lamda_B = 0.05
        #probability of obstacle is  self.P_B = 0.8

        
    # Choose the subdquent aisle the robot will drive down
    def chooseAisle(self, startCellCoords, goalCellCoords):
        
        lowestCost = 999999
        candidateAisle = None

        for aisle in Aisle:
            if self.aisleToDriveDown == aisle:
                continue

            candidatePath = self.planPathToGoalViaAisle(startCellCoords, goalCellCoords, aisle)
            print("================")
            print("New path drives into "+str(aisle))
            print("candidatePath.travelCost="+str(candidatePath.travelCost))
            if candidatePath.travelCost < lowestCost:
                lowestCost = candidatePath.travelCost
                candidateAisle = aisle
        self.alter_aisle_lowestCost = lowestCost
        print("================")
        print("New path drives into "+str(candidateAisle))
        print("================")
        return candidateAisle

    # Return whether the robot should wait for the obstacle to clear or not.
    def shouldWaitUntilTheObstacleClears(self, startCellCoords, goalCellCoords):
        L_w = 2
        if self.aisleToDriveDown is None:
            self.aisleToDriveDown = Aisle.B
        
        findWalkedPath = self.planner.search(self.startPos, startCellCoords)
        walkedPath = self.planner.extractPathToGoal()
        currentCost = walkedPath.travelCost

        origin_path_remaining_cost = self.currentPlannedPath.travelCost - currentCost

        newAisle = self.chooseAisle(startCellCoords, goalCellCoords)
        self.aisleToDriveDown = newAisle

        new_path_cost = self.alter_aisle_lowestCost
        print("==================================")
        #print(currentCoords[0], currentCoords[1])
        print(startCellCoords[0], startCellCoords[1])
        print(currentCost)  
        print("Remaining cost of original plan is " + str(origin_path_remaining_cost) + \
        ", new planned path's cost is " + str(new_path_cost) )        
        print("==================================")
        
        time_worth_to_wait = (new_path_cost - origin_path_remaining_cost) / L_w
        expected_time = 1.0/self.lamda_B
        print("time to wait is " + str(time_worth_to_wait) + " seconds")
        print("Expected time for obstacle to vanish is "+ str(expected_time) + " seconds")   
        print("==================================")

        return expected_time < time_worth_to_wait

    # This method will wait until the obstacle has cleared and the robot can move.
    def waitUntilTheObstacleClears(self):
        ini_time = time.time()
        waypoints = self.currentPlannedPath.waypoints
        for waypoint in waypoints:
            dX = waypoint.coords[0]
            dY = waypoint.coords[1]

            while self.occupancyGrid.getCell(dX, dY) == 1:
                time.sleep(0.01)
        current_time = time.time()
        print("============================================")
        print("time waited is " + str(current_time - ini_time) + " seconds")        
        print("============================================")
    
    # Plan a path to the goal which will go down the designated aisle. The code, as
    # currently implemented simply tries to drive from the start to the goal without
    # considering the aisle.
    def planPathToGoalViaAisle(self, startCellCoords, goalCellCoords, aisle):

        # Note that, if the robot has waited, it might be tasked to drive down the
        # aisle it's currently on. Your code should handle this case.
        if self.aisleToDriveDown is None:
            self.aisleToDriveDown = aisle

        # Implement your method here to construct a path which will drive the robot
        # from the start to the goal via the aisle.
        CoordsOfaisle = {
            Aisle.A : (26, 30),
            Aisle.B : (43, 30),
            Aisle.C : (59, 30),
            Aisle.D : (74, 30),
            Aisle.E : (90, 30)
        }

        aisleCoord = CoordsOfaisle[aisle]

        #first half the path, from the starting point to the aisle.
        pathToAisle = self.planner.search(startCellCoords, aisleCoord)
        # If we can't reach the goal, give up and return
        if pathToAisle is False:
            rospy.logwarn("Could not find a path to the goal at (%d, %d)", \
                            aisleCoord[0], aisleCoord[1])
            return None

        # Extract the path
        currentPlannedPath = self.planner.extractPathToGoal()

        pathToGoal = self.planner.search(aisleCoord, goalCellCoords)    

        # If we can't reach the goal, give up and return
        if pathToGoal is False:
            rospy.logwarn("Could not find a path to the goal at (%d, %d)", \
                            goalCellCoords[0], goalCellCoords[1])
            return None
        Path_Aisle_Goal = self.planner.extractPathToGoal()
            
        currentPlannedPath.addToEnd(Path_Aisle_Goal)
        self.planner.searchGridDrawer.drawPathGraphicsWithCustomColour(currentPlannedPath, 'yellow')

        currentPlannedPath
        return currentPlannedPath

    # This method drives the robot from the start to the final goal. It includes
    # choosing an aisle to drive down and both waiting and replanning behaviour.
    # Note that driving down an aisle is like introducing an intermediate waypoint.

    def driveToGoal(self, goal):

        # Get the goal coordinate in cells
        goalCellCoords = self.occupancyGrid.getCellCoordinatesFromWorldCoordinates((goal.x,goal.y))

        # Set the start conditions to the current position of the robot
        pose = self.controller.getCurrentPose()
        start = (pose.x, pose.y)
        startCellCoords = self.occupancyGrid.getCellCoordinatesFromWorldCoordinates(start)
        self.startPos = startCellCoords
        # Work out the initial aisle to drive down
        aisleToDriveDown = self.chooseInitialAisle(startCellCoords, goalCellCoords)

        # Reactive planner main loop - keep iterating until the goal is reached or the robot gets
        # stuck.
        
        while rospy.is_shutdown() is False:

            # Plan a path from the robot's current position to the goal. This is called even
            # if the robot waited and used its existing path. This is more robust than, say,
            # stripping cells from the existing path.           
            
            print 'Planning a new path: start=' + str(start) + '; goal=' + str(goal)
            
            # Plan a path using the current occupancy grid
            self.gridUpdateLock.acquire()
            self.currentPlannedPath = self.planPathToGoalViaAisle(startCellCoords, goalCellCoords, aisleToDriveDown)
            self.gridUpdateLock.release()

            # If we couldn't find a path, give up
            if self.currentPlannedPath is None:
                return False

            # Drive along the path towards the goal. This returns True
            # if the goal was successfully reached. The controller
            # should stop the robot and return False if the
            # stopDrivingToCurrentGoal method is called.
            goalReached = self.controller.drivePathToGoal(self.currentPlannedPath, \
                                                          goal.theta, self.planner.getPlannerDrawer())

            rospy.logerr('goalReached=%d', goalReached)

            # If we reached the goal, return
            if goalReached is True:
                return True

            # An obstacle blocked the robot's movement. Determine whether we need to
            # wait or replan.

            # Figure out where we are
            pose = self.controller.getCurrentPose()
            start = (pose.x, pose.y)
            startCellCoords = self.occupancyGrid.getCellCoordinatesFromWorldCoordinates(start)

            # See if we should wait
            waitingGame = self.shouldWaitUntilTheObstacleClears(startCellCoords, goalCellCoords)

            # Depending upon the decision, either wait or determine the new aisle
            # we should drive down.
            if waitingGame is True:
                self.waitUntilTheObstacleClears()
            else:
                aisleToDriveDown = self.aisleToDriveDown

        return False
            
            
