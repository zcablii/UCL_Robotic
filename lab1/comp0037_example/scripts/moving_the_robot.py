#!/usr/bin/env python

import rospy
from geometry_msgs.msg  import Twist
from nav_msgs.msg import Odometry
from math import pow,atan2,sqrt,pi
from PyKDL import Rotation

class stdr_controller():

    def __init__(self):
        #Creating our node,publisher and subscriber
        rospy.init_node('stdr_controller', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/robot0/cmd_vel', Twist, queue_size=10)
        self.current_pose_subscriber = rospy.Subscriber('/robot0/odom', Odometry, self.current_pose_callback)
        self.current_pose = Odometry()
        self.distance_tolerance = 0.01
 
    def current_pose_callback(self, data):
        self.current_pose = data

    def angle_to_range(self, angle):
        if angle < -180:
            angle += 360
        if angle > 180:
            angle -= 360
        return angle

    def run(self):

        # Sleep for 1s before starting. This gives time for all the parts of stdr to start up
        rospy.sleep(1.0)
        steps = [[15,2,0],[15,2,90],[15,10,45],[15,14,90],[1,12,-90],[1,2,0]]

        vel_msg = Twist()
    
        pose = self.current_pose.pose.pose

        # Get the position vector. ROS uses nested types for generality, but it gets to be a bit
        # cumbersome
        position = pose.position

        # The pose returns the orientation as a quaternion, which is a 4D representation of 3D
        # rotations. We just want the heading angle, so some conversion is required.
        # 
        orientation = pose.orientation

        theta = 2 * atan2(orientation.z, orientation.w) * 180 / pi

        # Show the output
        rospy.loginfo('Current position, x: {}, y:{}, theta:{}'.format(position.x,
            position.y, theta))

        for eachstep in steps:

            gx = eachstep[0]
            gy = eachstep[1]
            go = eachstep[2]
            xDiff = round(gx,1) - round(position.x,1)
            yDiff = round(gy,1) - round(position.y,1)
            angleToGoal = atan2(yDiff, xDiff) * 180 / pi
            if xDiff ==0 :
                if yDiff == 0:
                    angleToGoal = theta
                elif yDiff > 0:
                    angleToGoal = 90
                else:
                    angleToGoal = -90
            if xDiff > 0:
                if yDiff ==0:
                    angleToGoal = 0
                else:
                    angleToGoal = atan2(yDiff, xDiff) * 180 / pi
            if xDiff < 0:
                if yDiff == 0:
                    angleToGoal = 180
                else:
                    angleToGoal = atan2(yDiff, xDiff) * 180 / pi

            aDiff1 = self.angle_to_range(angleToGoal - theta) 
            aDiff3 = self.angle_to_range(go - angleToGoal) 

            distance = sqrt(xDiff**2+yDiff**2)
            # phase 1, rotate to goal
            rot_v = 20.0  #max rotation speed
            t1 = aDiff1/rot_v
            if t1<0:
                t1 = 0 - t1
                rot_v = 0 - rot_v
            vel_msg.linear.x = 0
            vel_msg.angular.z = rot_v
            self.velocity_publisher.publish(vel_msg)
            rospy.sleep(t1)
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
            self.velocity_publisher.publish(vel_msg)

            #phase 2, go to goal
            lin_v = 2.0  #mac linear speed
            t2 = distance/lin_v
            vel_msg.linear.x = lin_v
            vel_msg.angular.z = 0
            self.velocity_publisher.publish(vel_msg)
            rospy.sleep(t2)
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
            self.velocity_publisher.publish(vel_msg)

            #phase 3, rotate to goal
            t3 = aDiff3/rot_v
            if t3<0:
                t3 = 0 - t3
                rot_v = 0 - rot_v
            vel_msg.linear.x = 0
            vel_msg.angular.z = rot_v
            self.velocity_publisher.publish(vel_msg)
            rospy.sleep(t3)
            vel_msg.linear.x = 0
            vel_msg.angular.z = 0
            self.velocity_publisher.publish(vel_msg)

            pose = self.current_pose.pose.pose
            position = pose.position
            orientation = pose.orientation
            theta = 2 * atan2(orientation.z, orientation.w) * 180 / pi
            rospy.loginfo('Current position, x: {}, y:{}, theta:{}'.format(position.x,
                position.y, theta))

            disError = sqrt((gx-position.x)**2+(gy-position.y)**2)
            oriError = self.angle_to_range(go-theta) 
            rospy.loginfo('Position error: {}, orientation error: {}'.format(disError, oriError))
        

        #try:
        #    lin_velocity = float(raw_input('Enter desired linear velocity: '))
        #    rot_velocity = float(raw_input('Enter desired rotational velocity: '))
        #    duration = float(raw_input('Enter desired duration: '))
        #    vel_msg.linear.x = lin_velocity
        #    vel_msg.angular.z = rot_velocity * pi / 180.0
        #    self.velocity_publisher.publish(vel_msg)
        #    rospy.sleep(duration)
        #except ValueError:
        #    rospy.loginfo('Illegal value entered; try again')

        #vel_msg.linear.x = 0.0
        #vel_msg.angular.z = 0.0
        #self.velocity_publisher.publish(vel_msg)
            

   
if __name__ == '__main__':
    try:
        #Testing our function
        x = stdr_controller()
        x.run()

    except rospy.ROSInterruptException: pass
