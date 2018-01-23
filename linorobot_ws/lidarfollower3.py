#! /usr/bin/env python
# Authors: Jun Yu (foundation), Paul & Abhimanyu (debugging), Brandon (debugging, P implementation, algorithm tweaks)

#Import all the required messages and packages
import rospy # rospy is the ROS package that allows it to interpret python
import math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


## FRONT OF XV-11 LIDAR IS OF INDEX 180 OUT OF 360

# Class object that does everything
class Follower:
    #Initialise Subscriber and Publisher and Twist
    def __init__(self):
        self.scan_sub=rospy.Subscriber('scan', LaserScan, self.scan_callback)
        self.cmd_vel_pub=rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.twist=Twist()

    def scan_callback(self,msg):
    #Initialise variables (Change these!)
        robotSpeed= 1 #This is more of an 'average' speed, it gets manipulated higher or lower later on. Default value is 0.5, 1 if you want to be adventurous
        coneOfVision = 120
        maxLinearSpeed = 0.80 #Set this to prevent overshoots (lino-1 max is 0.80)
        maxAngularSpeed = 1 #Set this to prevent overshoots (lino-1 max is 3.70)

        #Getting data from sensor
        self.range_data = msg.ranges

        #Define boundary from midpoint(assuming midpoint is the front)
        bound = coneOfVision/2  # This means that the cone of the robot's vision that matters is 60*2 = 120 degrees
        upperBound = len(self.range_data) / 2 + bound # We're now setting our upper bound, 180/2+bound = 150
        lowerBound = len(self.range_data) / 2 - bound # We're setting our lower bound, 180/2-bound = 30  ( 150 - 30 is 120 degrees of vision!)

        #Slice out the values to form a new list
        middleRange = self.range_data[lowerBound:upperBound]
        widerRange = self.range_data[(lowerBound-bound/2):(upperBound+bound/2)] # Slice a wider range (180 degrees of vision) for later use

        #Get index of the smallest distance value within the middle range (if distance > 7.5cm)
        minVal = min(x for x in middleRange if x>0.075)
        indexOfMin = middleRange.index(minVal)

        #Conditions and Cases

        #If the robot is further than 30cm from object but less than 1.75m, start following
        if middleRange[indexOfMin] > 0.3 and minVal < 1.75: 
            if indexOfMin>bound+15 and indexOfMin<bound*2: #Turn left if indexOfMin is above the bound (with 15 degrees of tolerance per side)
                self.twist.linear.x = robotSpeed*(minVal)*math.tanh(minVal/1.75)+0.1 #(P Control: Robot moves faster the further away it is. math.tanh: Close to sweet spot it'll slow down exponentially)
                self.twist.angular.z = 0.75*robotSpeed-0.33*(minVal/1.75) #Turning speed decays as tracked object moves further away
            elif indexOfMin<bound-15 and indexOfMin>0: #Turn left if indexOfMin is below the bound (with 15 degrees of tolerance per side)
                self.twist.linear.x = robotSpeed*(minVal)*math.tanh(minVal/1.75)+0.1
                self.twist.angular.z = -0.75*robotSpeed+0.33*(minVal/1.75)
            else:
                self.twist.linear.x = robotSpeed*(minVal)*math.tanh(minVal/1.75)+0.1 #Otherwise, just move forward
                self.twist.angular.z = 0

    #If the robot is too close (less than 25cm away), move away
        elif middleRange[indexOfMin] > 0 and middleRange[indexOfMin] <= 0.25:
            #Wider range is used here, changing the cone of vision to 180   
            minVal = min(x for x in widerRange if x>0.075)
            indexOfMin = widerRange.index(minVal)
            if indexOfMin>(bound*1.5)+20 and indexOfMin<bound*3: #Bounds change here! That's why I have bound*1.5 as widerRange changes the critical values
                self.twist.linear.x = -0.5*(1-(math.tanh(minVal/0.25))) #Robot moves backwards faster the closer it is (tanh smoothing)
                self.twist.angular.z = 0.66
            elif indexOfMin<(bound*1.5)-20 and indexOfMin>0: #Same here
                self.twist.linear.x = -0.5*(1-(math.tanh(minVal/0.25)))
                self.twist.angular.z = -0.66
            else:
                self.twist.linear.x = -0.75*(1-(math.tanh(minVal/0.25)))
                self.twist.angular.z = 0

        #Otherwise, if the robot is in the sweet spot, or too far away, do nothing but be open to rotating
        else:
            #Wider range is used here, changing the cone of vision to 180   
            minVal = min(x for x in widerRange if x>0.075)
            indexOfMin = widerRange.index(minVal)
            if indexOfMin>(bound*1.5)+15 and indexOfMin<bound*3: #Same deal as above
                self.twist.linear.x = 0
                self.twist.angular.z = 0.66
            elif indexOfMin<(bound*1.5)-15 and indexOfMin>0: #Same here
                self.twist.linear.x = 0
                self.twist.angular.z = -0.66
            else:
                self.twist.linear.x = 0
                self.twist.angular.z = 0


        #print("lenofrange: ", len(self.range_data))
        #print("lowerBound: ", lowerBound)
        #print("upperBound: ", upperBound)
        print("min range: ", minVal)
        #print("range data: ",self.range_data)
        print("indexOfMin:: ",indexOfMin)
        #print("increment: ",self.increment)
        #print("Linear X: ", self.twist.linear.x)
        #print("Angular Z: ", self.twist.angular.z)

        #Limit linorobot velocity messages to max speeds to prevent overshoots
        if self.twist.linear.x > maxLinearSpeed:
            self.twist.linear.x = maxLinearSpeed
        if self.twist.angular.z > maxAngularSpeed:
            self.twist.angular.z = maxAngularSpeed
        if self.twist.linear.x < -maxLinearSpeed:
            self.twist.linear.x = -maxLinearSpeed
        if self.twist.angular.z < -maxAngularSpeed:
            self.twist.angular.z = -maxAngularSpeed

        #Publish to cmd_vel (make the Linorobot move)   
        self.cmd_vel_pub.publish(self.twist)

#initialise Node
rospy.init_node('lidarfollower')

# invoke Class
follower = Follower()
rospy.spin()

# Random thoughts (From Jun Yu)
# check a certain range.
# flip range
# maintainfminimum
# check if lidar is on
# arduino joystick
