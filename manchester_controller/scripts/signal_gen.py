#!/usr/bin/env python 
import rospy
from geometry_msgs.msg import Pose2D

msg = Pose2D()

pub = rospy.Publisher('pose2D', Pose2D, queue_size=10)
rospy.init_node('signal_generator')

r = rospy.Rate(10) # 10hz
while not rospy.is_shutdown():
    
    msg.x = input("position in x: ")
    msg.y = input("position in y: ")
    pub.publish(msg)
    r.sleep()