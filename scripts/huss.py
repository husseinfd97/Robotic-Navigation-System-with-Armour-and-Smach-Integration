#!/usr/bin/env python

import roslib
import random
import math
import time
import rospy
import rospkg
import smach
import smach_ros
from std_msgs.msg import Bool
from armor_api.armor_client import ArmorClient


NOT_YET_UPLOADED= 'NOT_YET_UPLODED'
UPLOADED='UPLOADED'
global map_Uploaded_flag=0
global battery_charged_flag=0
global urgent_room_flag=0

# define state Foo
class loading_map(smach.State):

   def __init__(self):
        smach.State.__init__(self, outcomes=[NOT_YET_UPLOADED, UPLOADED])

    def execute(self, userdata):
        #mutex remain 
        if map_Uploaded_flag==0:
            return NOT_YET_UPLOADED
        elif map_Uploaded_flag==1:
            return UPLOADED   



class moving_in_corridoor(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['keep_moving_in_cooridoor','urgent room exist','battery low'])
        self.counter = 0

    def execute(self, userdata):
        if battery_charged_flag==0:
            return 'battery low'

        elif battery_charged_flag==1:
            if urgent_room_flag==1:
                return 'urgent room exist'
            elif urgent_room_flag ==0:
                #here should keep mving bet c1 and c2
                return 'keep_moving_in_cooridoor'


        


        

# define state Bar
class move_to_urgent_room(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['keep visiting rooms','no urgent room','battery low'])

    def execute(self, userdata):
        if battery_charged_flag==0:
            return 'battery low'
        elif  battery_charged_flag==1:
            if urgent_room_flag==1:
                #robot should visit the urgent rooms 
                return 'keep visiting rooms'
            elif urgent_room_flag ==0:
                return 'no urgent room'

        

# define state Bar
class Recharging(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['keep charging battery','battery charged'])


    def execute(self, userdata):
        if battery_charged_flag==0:
            return 'keep charging battery'
        elif battery_charged_flag==1: 
            return 'battery charged'



        




def main():
    rospy.init_node('smach_example_state_machine')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['outcome4'])

    # Open the container
    with sm:
    'keep charging battery','battery charged'
        # Add states to the container
        smach.StateMachine.add('loading_map', loading_map(), 
                                transitions={NOT_YET_UPLOADED:'loading_map', UPLOADED:'moving_in_corridoor'})
        smach.StateMachine.add('moving_in_corridoor', moving_in_corridoor(), 
                                transitions={'keep_moving_in_cooridoor':'moving_in_corridoor','urgent room exist':'move_to_urgent_room','battery low':'Recharging'})
        smach.StateMachine.add('move_to_urgent_room', move_to_urgent_room(), 
                                transitions={'keep visiting rooms':'move_to_urgent_room', 'no urgent room':'moving_in_corridoor','battery low':'Recharging'})
        smach.StateMachine.add('Recharging', Recharging(), 
                                transitions={'keep charging battery':'Recharging','battery charged':'moving_in_corridoor' })

    # Create and start the introspection server for visualization
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()

    # Execute the state machine
    outcome = sm.execute()

    # Wait for ctrl-c to stop the application
    rospy.spin()
    sis.stop()



if __name__ == '__main__':
    main()