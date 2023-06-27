#!/usr/bin/env python

# Use randomness for testing purposes.
import random

# Imports relative to ROS and the SMACH library.
import rospy
import smach_ros
from smach import StateMachine, State
from load_ontology.py import LoadMap



NOT_YET_UPLOADED= "NOT_YET_UPLODED"
UPLOADED="UPLOADED"

LOOP_SLEEP_TIME = 0.3


global current_pos
global available_pos
global map_Uploaded_flag = 0

class loading_map(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=[NOT_YET_UPLOADED, UPLOADED])

    def execute(self, userdata):
        #mutex remain 
        #print(' waiting for the map to be uploded ')
        map_Uploaded_flag=LoadMap()
        rospy.sleep(sleeptime)
        if map_Uploaded_flag == 0:
            return NOT_YET_UPLOADED
        else:
            return UPLOADED

# The definition of the recharging state.
class Recharging(State):
    # Construct this class, i.e., initialise this state.
    #acquiring something from 
    def __init__(self, interface_helper):
        # Get a reference to the interfaces with the other nodes of the architecture.
        self._helper = interface_helper
        # Initialise this state with possible transitions (i.e., valid outputs of the `execute` function).
        State.__init__(self, outcomes=[ROBOT_RECHARGED])

    # Define the function performed each time a transition is such to enter in this state.
    # Note that the input parameter `userdata` is not used since no data is required from the other states.
    def execute(self, userdata):
        while not rospy.is_shutdown():  # Wait for stimulus from the other nodes of the architecture.
            # Acquire the mutex to assure data consistencies with the ROS subscription threads managed by `self._helper`.
            self._helper.mutex.acquire()
            client.manipulation.add_objectprop_to_ind("isIn", "Robot1", "E")
            client.utils.apply_buffered_changes()
            client.utils.sync_buffered_reasoner()
            try:
                # If the battery is no low anymore take the `charged` transition.
                if not self._helper.is_battery_low():
                    self._helper.reset_states()  # Reset the state variable related to the stimulus.
                    return ROBOT_RECHARGED
            finally:
                # Release the mutex to unblock the `self._helper` subscription threads if they are waiting.
                self._helper.mutex.release()
            # Wait for a reasonably small amount of time to allow `self._helper` processing stimulus (eventually).
            rospy.sleep(LOOP_SLEEP_TIME)


#where is the robot ? 
current_pos=(client.query.objectprop_b2_ind("isIn", "Robot1")[0])[32:-1]
#where can the robot reach ? 
available_pos=client.query.objectprop_b2_ind("canReach", "Robot1")
one_available=random.choice(available_pos)
while not(one_available = current_pos)
    one_available=random.choice(available_pos)
client.manipulation.add_objectprop_to_ind("isIn", "Robot1", one_available)
client.utils.apply_buffered_changes()
client.utils.sync_buffered_reasoner()



# define state Where to go 
class Robot_planner(State):
    def __init__(self, interface_helper):
            # Get a reference to the interfaces with the other nodes of the architecture.
            self._helper = interface_helper
            # Initialise this state with possible transitions (i.e., valid outputs of the `execute` function).
            State.__init__(self, outcomes=[ROBOT_RECHARGED])# change to (from load robot)
        
    def execute(self, userdata):
        # function called when exiting from the node, it can be blacking
        time.sleep(5)
        #rospy.loginfo('Executing state UNLOCKED (users = %f)'%userdata.unlocked_counter_in)
        #userdata.unlocked_counter_out = userdata.unlocked_counter_in + 1
        return user_action()

def main()
    rospy.sleep(15)
    rospy.init_node('Finite_S_M')
    sm_main = StateMachine([])
        # Create a SMACH state machine
        robot = smach.StateMachine(outcomes=['Interface'])
        smach.StateMachine.add('waiting_for_map', waiting_for_map(), 
                                transitions={'keepwaiting':'waiting_for_map','maploaded':'move_in_corridor'})
    '''
def main():
    # Initialise this ROS node.
    rospy.init_node(anm.NODE_BEHAVIOUR, log_level=rospy.INFO)
    # Initialise an helper class to manage the interfaces with the other nodes in the architectures, i.e., it manages external stimulus.
    helper = InterfaceHelper()

    # Get the initial robot pose from ROS parameters.
    #robot_pose_param = rospy.get_param(anm.PARAM_INITIAL_POSE, [0, 0])
    # Initialise robot position in the `robot_state`, as required by the plan anc control action servers.
    #helper.init_robot_pose(Point(x=robot_pose_param[0], y=robot_pose_param[1]))

    # Get the user's position from ROS parameters.
    #user_pose_param = rospy.get_param(anm.PARAM_USER_POSE, [0, 0])
    #user_pose = Point(x=user_pose_param[0], y=user_pose_param[1])

    # Define the structure of the Finite State Machine.
    sm_main = StateMachine([])
    with sm_main:
        # Define the higher level node for the normal behaviour, i.e., when the robot moves between random points.
        sm_normal = StateMachine(outcomes=[TRANS_REPEAT, TRANS_BATTERY_LOW, TRANS_CALLED])
        with sm_normal:
            # Define the inner state to plan the via-points toward a random position.
            StateMachine.add(STATE_PLAN_TO_RANDOM_POSE, PlanToRandomPose(helper),
                             transitions={TRANS_PLANNED_TO_RANDOM_POSE: STATE_GO_TO_RANDOM_POSE,
                                          TRANS_RECHARGING: TRANS_BATTERY_LOW,
                                          TRANS_START_INTERACTION: TRANS_CALLED})
            # Define the inner state to move to a random position.
            StateMachine.add(STATE_GO_TO_RANDOM_POSE, GoToRandomPose(helper),
                             transitions={TRANS_WENT_RANDOM_POSE: TRANS_REPEAT,
                                          TRANS_RECHARGING: TRANS_BATTERY_LOW,
                                          TRANS_START_INTERACTION: TRANS_CALLED})
        # Add the sub Finite State Machine to the main Finite State Machine concerning the `normal` behaviour.
        StateMachine.add(STATE_NORMAL, sm_normal,
                         transitions={TRANS_REPEAT: STATE_NORMAL,
                                      TRANS_BATTERY_LOW: STATE_RECHARGING,
                                      TRANS_CALLED: STATE_INTERACT})

        # Define the higher level node for the interaction behaviour, i.e., when the robot moves to the user first,
        # and then to the location pointed by the user.
        sm_interact = StateMachine(outcomes=[TRANS_REPEAT, TRANS_BATTERY_LOW, TRANS_GREETED])
        with sm_interact:
            # Define the inner state to plan the via-points toward the user.
            StateMachine.add(STATE_PLAN_TO_USER, PlanToUser(helper, user_pose),
                             transitions={TRANS_PLANNED_TO_USER: STATE_GO_TO_USER,
                                          TRANS_RECHARGING: TRANS_BATTERY_LOW,
                                          TRANS_STOP_INTERACTION: TRANS_GREETED})
            # Define the inner state to move toward the user.
            StateMachine.add(STATE_GO_TO_USER, GoToUser(helper),
                             transitions={TRANS_WENT_TO_USER: STATE_PLAN_TO_GESTURE,
                                          TRANS_RECHARGING: TRANS_BATTERY_LOW,
                                          TRANS_STOP_INTERACTION: TRANS_GREETED})
            # Define the inner state to plan the via-points toward the location pointed by the user.
            StateMachine.add(STATE_PLAN_TO_GESTURE, PlanToGesture(helper),
                             transitions={TRANS_PLANNED_TO_GESTURE: STATE_GO_TO_GESTURE,
                                          TRANS_RECHARGING: TRANS_BATTERY_LOW,
                                          TRANS_STOP_INTERACTION: TRANS_GREETED})
            # Define the inner state to move toward the location pointed by the user.
            StateMachine.add(STATE_GO_TO_GESTURE, GoToGesture(helper),
                             transitions={TRANS_WENT_TO_GESTURE: TRANS_REPEAT,
                                          TRANS_RECHARGING: TRANS_BATTERY_LOW,
                                          TRANS_STOP_INTERACTION: TRANS_GREETED})
        # Add the sub Finite State Machine to the main Finite State Machine concerning the `interaction` behaviour.
        StateMachine.add(STATE_INTERACT, sm_interact,
                         transitions={TRANS_REPEAT: STATE_INTERACT,
                                      TRANS_BATTERY_LOW: STATE_RECHARGING,
                                      TRANS_GREETED: STATE_NORMAL})

        # Define the node where the robot's will recharge itself.
        StateMachine.add(STATE_RECHARGING, Recharging(helper),
                         transitions={TRAMS_RECHARGED: STATE_NORMAL})

    # Create and start the introspection server for visualizing the finite state machine.
    sis = smach_ros.IntrospectionServer('sm_introspection', sm_main, '/SM_ROOT')
    sis.start()

    # Execute the state machine. Note that the `outcome` value of the main Finite State Machine is not used.
    outcome = sm_main.execute()

    # Wait for ctrl-c to stop the application
    rospy.spin()
    sis.stop()


# The function that get executed at start time.
if __name__ == '__main__':
    main()  # Initialise and start the ROS node.

'''

