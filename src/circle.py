#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Pose, Quaternion, Point, PoseStamped, PoseWithCovariance, TwistWithCovariance, Twist, Vector3, Wrench
from gazebo_msgs.srv import ApplyBodyWrench, GetModelState
import tf.transformations as tft
from numpy import float64

def main():
    #pub = rospy.Publisher('acrobot_package/cmd_vel', Twist, queue_size=10)
    #rospy.init_node('circler', anonymous=True)
    #rate = rospy.Rate(2) # 10hz
    rospy.wait_for_service('/gazebo/apply_body_wrench')
    apply_body_wrench = rospy.ServiceProxy('/gazebo/apply_body_wrench', ApplyBodyWrench)
    get_model_state = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)

    point = Point()
    point.x = 0
    point.y = 0
    point.z = -0.400

    wrench = Wrench()
    wrench.force.x = 0
    wrench.force.y = 10
    wrench.force.z = 0
    wrench.torque.x = 0
    wrench.torque.y = 0
    wrench.torque.z = 0

    while not rospy.is_shutdown():
        try:
            wrench.force.y = -wrench.force.y
            apply_body_wrench(body_name = "acrobot::link_0",
                reference_frame = "acrobot::link_0",
                reference_point = point,
                wrench = wrench,
                duration = rospy.Duration(.5))
            acrobot_state = get_model_state("acrobot_model", 'world')
            print "\n"
            print "Status.success = ", acrobot_state.success
            print "X: ", str(acrobot_state.pose.position.x)
            print "Y: ", str(acrobot_state.pose.position.y)
            print "Z: ", str(acrobot_state.pose.position.z)
            print "done"
        except rospy.ServiceException as e:
            print e
        rospy.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
