#!/usr/bin/env python   
import rospy
import numpy as np
import math
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose2D
msg = Twist()
#velocidad = distancia /tiempo
#tiempo = distancia/velocidad

#angular en z es 1 para la izquierda -1 para la derecha
cordX = 0
cordY = 0
lastCordX = 0
lastCordY = 0
velocidad = 0.5

count = 0

grados = 0
distancia = 0
lastGrado = 0
def angle_distance(cordX, cordY):
    global lastCordX, lastCordY, grados, distancia, count, lastGrado
    
    if count == 0:
        grados = math.atan2(cordY,cordX)
        lastGrado = grados
    else:
        grados = math.atan2(cordY,cordX)
        grados = grados -lastGrado
        if grados < 0:
            grados = np.pi+grados
        lastGrado = grados
    
    distancia = math.sqrt((lastCordY-cordY)**2+(lastCordX-cordX)**2)
    lastCordY = cordY
    lastCordX = cordX
    rospy.loginfo("distancia: %f, grados: %f", distancia, grados)
    count += 1

def cb_position(data):
    global cordX, cordY, ti
    cordX = data.x
    cordY = data.y
    ti = rospy.get_time()
    angle_distance(cordX, cordY)


if __name__=='__main__':
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rospy.Subscriber("pose2D", Pose2D, cb_position)
    rospy.init_node('controller')

    r = rospy.Rate(10) # 10hz
    r.sleep()
    ti = rospy.get_time()

    go = False
    while not rospy.is_shutdown():
        t = rospy.get_time()-ti
        tMax = distancia/velocidad
        if t < grados and go == False:
            #print(t, grados)
            msg.linear.x = 0.0
            msg.angular.z = 1.0
            #rospy.loginfo("tiempo giro: %f", t)
        else:
            msg.angular.z = 0.0
            go = True
            

        if t <= tMax and go == True:
            msg.linear.x = 0.5
            #rospy.loginfo("tiempo recta: %f", t)   
        else:     
            msg.linear.x = 0.0
            go = False
            
 

        #print(t)
        #print(grados)
        pub.publish(msg)
        r.sleep()   