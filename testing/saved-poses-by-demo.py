"""
Saved pose node
    + Perform the saved poses for the joints

    + Move to bag pose
        - after confirmation of from the user on the navigation
        - call to start the aruco marker adjustment of the gripper

    + grip and remove bag pose
        - after confirmation from the user on the gripper location 
        - perform the removal of the bag and 
        - send signal to front-end to indicate the bag is removed 
        - send singnal to navigation to move to bin
    
    + throw away bag
        - after signal from navigation
        - release gripper
        - send signal to navigation to return to initial position
"""


import stretch_body.arm
import stretch_body.lift
import stretch_body.stretch_gripper as gripper
import time
from stretch_body.hello_utils import *
import stretch_body.wrist_yaw as wrist

poses = {
    # 'initial':(0.5615861676470746, 0.24211288835998443, 4.310486013958652, 0.08053399136399617),
    # 'at-bag': (0.4795945004727337, 0.24211526939820244, 4.310486013958652, 0.08053399136399617),
    # 'close gripper': (0.479591149126581, 0.2421176766016756, -7.884661249732196, 0.08053399136399617),


    # 'remove and lift': (0.7307844880308441, 0.0027174925323322544, -7.884661249732196, 2.14629478571666)

    'throw-bag': (0.7305178374456467, 0.2614214337317741, 4.310486013958652, -0.23648870479903633)
}
w = wrist.WristYaw()
l = stretch_body.lift.Lift()
l.motor.disable_sync_mode()


a = stretch_body.arm.Arm()
a.motor.disable_sync_mode()

g = gripper.StretchGripper()

# if not w.startup():
#     exit()
if not (l.startup() and g.startup(threaded=False) and a.startup() and w.startup(threaded=False)):
    exit() # failed to start arm!

while True:
# Wait for the user to hit the space bar
    user_in = input("Hit c to close gripper\n"
                    + "Hit x to open gipper\n"
                    + "Hit o to move gripper left\n"
                    + "Hit p to move right gipper\n"
                    + "Hit space to save pose\n"
                    + "Hit r to play poses\n")

    if user_in == 'c':
        # close 
        g.move_to(-100)
        time.sleep(2)
    elif user_in == 'x':
        g.move_to(100)
        time.sleep(2)
        # open
    elif user_in == 'o':
        #left
        w.move_by(0.3)
        time.sleep(2)
    elif user_in == 'p':
        w.move_by(-0.3)
        time.sleep(2)
    elif user_in == ' ':
        pose_name = input("Enter a name for the pose: ")
        g.pull_status()
        w.pull_status()
        poses[pose_name] = (l.status['pos'], a.status['pos'], g.status['pos'], w.status['pos'])
        print(f"Position: {l.status['pos']}, {a.status['pos']}, {g.status['pos']}, {w.status['pos']}")
    elif user_in == 'r':
        for pose_name, pose_pos in poses.items():
            # Get the position values for the pose
            lift_pos, arm_pos, grip_pos, wrist_pos = pose_pos
            # Print the position values for the pose
            print(f"Pose '{pose_name}':")
            print(f"  Lift position: {lift_pos}")
            print(f"  Arm position: {arm_pos}")
            print(f"  Grip position: {grip_pos}")
            print(f"  Wrist position: {wrist_pos}")
            l.move_to(lift_pos)
            l.motor.wait_until_at_setpoint()
            l.push_command()
            a.move_to(arm_pos)
            a.push_command()
            a.motor.wait_until_at_setpoint()
            w.move_to(wrist_pos)
            time.sleep(2)
            if grip_pos < 0:
                # close
                g.move_to(-100)
            else:
                g.move_to(100)
            time.sleep(3)
        

        

