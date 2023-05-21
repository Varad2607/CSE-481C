#!/usr/bin/env python3

import rospy
from move_base_msgs.msg import MoveBaseActionGoal
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped, String
"""
Navigation Node
    + Based on the user's singnal, start navigation of robot to the desired location

    + navigate_to_patient
        - send /initialpose to navigation for localization
        - send /move_base/goal as the goal location & orientation
    
    + navigate_to_bin
        - send move_base/goalas the goal location & orientation
        - send singal to saved-poses to perform thowing away
    
    + navigate_to_initial
        - return to the inital position
"""
class NavigationNode:
    def __init__(self):
        rospy.init_node('navigation_node')

        # Create publishers for sending goals
        self.initialpose_pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=10)
        self.movebase_goal_pub = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size=10)
        self.throwing_signal_pub = rospy.Publisher('/throwing_signal', String, queue_size=10)

        # Set the rate at which to publish messages (adjust as needed)
        self.rate = rospy.Rate(1)

    def navigate_to_patient(self):
        # Send /initialpose to navigation for localization
        initial_pose = PoseWithCovarianceStamped()

        # Set the position and orientation values
        initial_pose.position.x = 1.1394891066611121
        initial_pose.position.y = -2.8552935343172003
        initial_pose.orientation.z = 0.707
        self.initialpose_pub.publish(initial_pose)
        rospy.sleep(1)  # Wait for the message to be published

        # Send /move_base/goal as the goal location & orientation
        goal_pose = PoseStamped()
        # Set the goal pose details
        goal_pose.pose.position.x = 0.174
        goal_pose.pose.position.y = 4.27
        goal_pose.pose.orientation.z = 0.707

        movebase_goal = MoveBaseActionGoal()
        movebase_goal.header.stamp = rospy.Time.now()
        movebase_goal.header.frame_id = ''
        movebase_goal.goal = goal_pose

        self.movebase_goal_pub.publish(movebase_goal)

    def navigate_to_bin(self):
        # Send /move_base/goal as the goal location & orientation
        goal_pose = PoseStamped()
        # Set the goal pose details
        # ...

        movebase_goal = MoveBaseActionGoal()
        movebase_goal.header.stamp = rospy.Time.now()
        movebase_goal.header.frame_id = ''
        movebase_goal.goal = goal_pose

        self.movebase_goal_pub.publish(movebase_goal)

        # Send signal to saved-poses to perform throwing away
        signal = "throw"
        self.throwing_signal_pub.publish(signal)

    def navigate_to_initial(self):
        # Return to the initial position
        initial_pose = PoseStamped()
        # Set the initial pose details
        # ...

        movebase_goal = MoveBaseActionGoal()
        movebase_goal.header.stamp = rospy.Time.now()
        movebase_goal.header.frame_id = ''
        movebase_goal.goal = initial_pose

        self.movebase_goal_pub.publish(movebase_goal)

    def run(self):
        while not rospy.is_shutdown():
            # Based on the user's signal, start navigation of the robot to the desired location
            user_signal = input("Enter signal (patient/bin/initial): ")

            if user_signal == "patient":
                self.navigate_to_patient()
            elif user_signal == "bin":
                self.navigate_to_bin()
            elif user_signal == "initial":
                self.navigate_to_initial()
            else:
                rospy.logwarn("Invalid signal entered.")

            self.rate.sleep()

if __name__ == '__main__':
    try:
        nav_node = NavigationNode()
        nav_node.run()
    except rospy.ROSInterruptException:
        pass