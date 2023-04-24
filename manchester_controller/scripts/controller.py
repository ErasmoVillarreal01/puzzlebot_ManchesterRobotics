#!/usr/bin/env python   
import rospy
import numpy as np
from geometry_msgs.msg import Twist
msg = Twist()
#velocidad = distancia /tiempo
#tiempo = distancia/velocidad
#def square():
#    if(tiempo ==4)

#angular en z es 1 para la izquierda -1 para la derecha
velocidad = 0.5
distancia = 2
tMax = distancia/velocidad
if __name__=='__main__':
   #Initialise and Setup node
   
   #Setup Publishers and subscribers here
   #Initiate the node called controller, and create de pub and subs
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.init_node('controller')
    msg.linear.x = 0.5
   
    r = rospy.Rate(10) # 10hz
    r.sleep()
    ti = rospy.get_time()
    while not rospy.is_shutdown():
        t = rospy.get_time()-ti

        if t < tMax:
            msg.linear.x = 0.5
            msg.angular.z = 0.0
            rospy.loginfo("tiempo recta: %d", t)
        elif t >= tMax:
            msg.linear.x = 0.0
            msg.angular.z = 1.0
            rospy.loginfo("tiempo giro: %d", t)
            if t > tMax + np.pi/2:
                ti = rospy.get_time()
        
        rospy.loginfo(t)
        #square()
        pub.publish(msg)
        r.sleep()   