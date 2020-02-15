#!/usr/bin/env python
import rospy
from geometry_msgs.msg  import Twist
from geometry_msgs.msg  import Pose
from math import pow,atan2,sqrt
from comp0037_planner_controller.planned_path import PlannedPath
from comp0037_planner_controller.controller_base import ControllerBase
import math
import angles
import datetime

# This sample controller works a fairly simple way. It figures out
# where the goal is. It first turns the robot until it's roughly in
# the correct direction and then keeps driving. It monitors the
# angular error and trims it as it goes.

class Move2GoalController(ControllerBase):

    def __init__(self, occupancyGrid):
        ControllerBase.__init__(self, occupancyGrid)
        
        # Get the proportional gain settings
        self.distanceErrorGain = rospy.get_param('distance_error_gain', 1)
        self.angleErrorGain = rospy.get_param('angle_error_gain', 4)
        self.driveAngleErrorTolerance = math.radians(rospy.get_param('angle_error_tolerance', 1))
        #for total distance
        self.prevX = self.pose.x
        self.prevY = self.pose.y
        self.disTraveled = 0
        #for total angle
        self.prevAngle = self.pose.theta
        self.totAngle = 0
        #for total time
        self.currentTime = datetime.datetime.now()
        self.totTime = 0.0

    def get_distance(self, goal_x, goal_y):
        distance = sqrt(pow((goal_x - self.pose.x), 2) + pow((goal_y - self.pose.y), 2))
        return distance

    def shortestAngularDistance(self, fromAngle, toAngle):
        delta = toAngle - fromAngle
        if (delta < -math.pi):
            delta = delta + 2.0*math.pi
        elif(delta > math.pi):
            delta = delta - 2.0*math.pi
        return delta
        
    def driveToWaypoint(self, waypoint):
        vel_msg = Twist()
        #for total distance
        dX = self.prevX - self.pose.x
        dY = self.prevY - self.pose.y
        self.prevX = self.pose.x
        self.prevY = self.pose.y
        self.disTraveled = self.disTraveled + sqrt(dX * dX + dY * dY)
        #for total angle
        self.totAngle = self.totAngle + abs(self.shortestAngularDistance(self.prevAngle, self.pose.theta))
        self.prevAngle = self.pose.theta
        totAngleTurned = self.totAngle/math.pi*360.0
        #for total time
        tempTime = datetime.datetime.now()
        dT = tempTime - self.currentTime
        self.totTime = self.totTime + dT.seconds + dT.microseconds*(10**(-6))
        self.currentTime = tempTime

        dX = waypoint[0] - self.pose.x
        dY = waypoint[1] - self.pose.y
        distanceError = sqrt(dX * dX + dY * dY)
        angleError = self.shortestAngularDistance(self.pose.theta, atan2(dY, dX))
       
        while (distanceError >= self.distanceErrorTolerance) & (not rospy.is_shutdown()):
            #print("Current Pose: x: {}, y:{} , theta: {}\nGoal: x: {}, y: {}\n".format(self.pose.x, self.pose.y,
            #                                                                           self.pose.theta, waypoint[0],
            #                                                                           waypoint[1]))
            print("Distance Error: {}\nAngular Error: {}\nDistance Travelled: {}\nAngle turned: {}\nTime past: {}".format(distanceError, angleError, self.disTraveled, totAngleTurned, self.totTime))

            # Proportional Controller
            # linear velocity in the x-axis: only switch on when the angular error is sufficiently small
            if math.fabs(angleError) < self.driveAngleErrorTolerance:
                vel_msg.linear.x = max(0.0, min(self.distanceErrorGain * distanceError, 10.0))
                vel_msg.linear.y = 0
                vel_msg.linear.z = 0

            # angular velocity in the z-axis:
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = max(-5.0, min(self.angleErrorGain * angleError, 5.0))


            #print("Linear Velocity: {}\nAngular Velocity: {}\n\n".format(vel_msg.linear.x, math.degrees(vel_msg.angular.z)))
            # Publishing our vel_msg
            self.velocityPublisher.publish(vel_msg)
            if (self.plannerDrawer is not None):
                self.plannerDrawer.flushAndUpdateWindow()
                
            self.rate.sleep()

            distanceError = sqrt(pow((waypoint[0] - self.pose.x), 2) + pow((waypoint[1] - self.pose.y), 2))
            angleError = self.shortestAngularDistance(self.pose.theta,
                                                      atan2(waypoint[1] - self.pose.y, waypoint[0] - self.pose.x))
            #for total distance
            dX = self.prevX - self.pose.x
            dY = self.prevY - self.pose.y
            self.prevX = self.pose.x
            self.prevY = self.pose.y
            self.disTraveled = self.disTraveled + sqrt(dX * dX + dY * dY)
            #for total angle
            self.totAngle = self.totAngle + abs(self.shortestAngularDistance(self.prevAngle, self.pose.theta))
            totAngleTurned = self.totAngle/math.pi*360.0
            self.prevAngle = self.pose.theta
            #for total time
            tempTime = datetime.datetime.now()
            dT = tempTime - self.currentTime
            self.totTime = self.totTime + dT.seconds + dT.microseconds*(10**(-6))
            self.currentTime = tempTime

        # Make sure the robot is stopped once we reach the destination.
        vel_msg.linear.x = 0
        vel_msg.angular.z = 0
        self.velocityPublisher.publish(vel_msg)

    def rotateToGoalOrientation(self, goalOrientation):
        vel_msg = Twist()

        goalOrientation = math.radians(goalOrientation)

        angleError = self.shortestAngularDistance(self.pose.theta, goalOrientation)

        while (math.fabs(angleError) >= self.goalAngleErrorTolerance) & (not rospy.is_shutdown()):
            #print 'Angular Error: ' + str(angleError)

            # angular velocity in the z-axis:
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = max(-5.0, min(self.angleErrorGain * angleError, 5.0))

            # Publishing our vel_msg
            self.velocityPublisher.publish(vel_msg)
            if (self.plannerDrawer is not None):
                self.plannerDrawer.flushAndUpdateWindow()
                
            self.rate.sleep()
            angleError = self.shortestAngularDistance(self.pose.theta, goalOrientation)

        # Stop movement once finished
        vel_msg.angular.z = 0
        self.velocityPublisher.publish(vel_msg)