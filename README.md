# First Assignment of Experimental Robotic Laboratory 

## Introduction
This assignment project focuses on implementing a robotic system using the Armour package which is resposible for manipulating online OWL ontologies and Smach package which is resposible for building hierarchical state machines decribing the diffrent staes of the robot. The system aims to simulate a robot operating in a 2D environment consisting of four rooms and three corridors. The robot's behavior is designed to navigate through the environment, visiting different locations while following certain policies.

## Environment
The 2D environment is composed of four rooms and three corridors. The rooms are labeled as R1, R2, R3, and R4, while the corridors are labeled as C1, C2, and E. The robot moves within this environment, with various doors (D1...D7) connecting the rooms and corridors as it's shown in the figure.

![map](https://github.com/husseinfd97/as_1/assets/94136236/436afa1a-d339-459e-abae-127e8ce39b74)


The indoor environment comprises various entities, such as doors, rooms, and corridors, with interconnected relationships. When two locations share a common door, it implies a connection between them denoted by the "connectedTo" relation. Furthermore, rooms that have not been visited for a specified duration, defined by the urgency threshold, are designated as urgent. These relationships and urgency status provide important contextual information about the environment, facilitating navigation and decision-making processes for the robot.

## Robot Behavior and Logic
The robot's behavior can be divided into two phases:

### Phase 1: Building the Topological Map
The robot starts in the E location and waits until it receives information to build the topological map. This information includes the relations between C1, C2, R1, R2, R3 locations, and the doors D1...D6.

### Phase 2: Navigating and Visiting Locations
After building the topological map, the robot moves to a new location and waits for some time before visiting another location. This behavior is repeated in an infinite loop. When the robot's battery is low, it returns to the E location and waits for some time before starting the behavior again.

The surveillance policy for the robot's movement is as follows:
- When the robot's battery is not low, it primarily stays on corridors.
- If a reachable room has not been visited for some time, the robot should visit it.

The implemented code ensures that the robot follows this behavior and policy by incorporating the necessary functions and logic.

## Software Architecture
The software architecture of the project consists of three nodes:

1. Load Map Node: Responsible for loading the topological map and publishing the load_map status.
2. State Machines Node: Implements the finite state machine (FSM) that controls the robot's behavior and actions. It subscribes to the load_map and battery_state topics, updates the urgent_room_flag and location_updated flags, and performs the necessary actions such as moving in the corridor, moving to urgent rooms, and recharging.
3. Battery Node: Publishes the battery_state status periodically, indicating the current battery level of the robot.

### Temporal Diagram
A temporal diagram illustrates the sequence of interactions between the nodes, showcasing how the load_map, urgent_room_flag, location_updated, and battery_state are published and utilized by the state machines node.
![tem](https://github.com/husseinfd97/as_1/assets/94136236/6cb13115-be0c-4410-95e4-463fb46574e6)

### State Diagrams
State diagrams provide a visual representation of the different states and transitions in the state machines node. They illustrate the flow and decision-making process of the finite state machine.
![state](https://github.com/husseinfd97/as_1/assets/94136236/5dfc741c-b03b-4465-976f-4ad46530faf6)

### Running Code


https://github.com/husseinfd97/as_1/assets/94136236/b06a0333-c87e-410e-a0a3-e460f4481a58

## Dependencies

In order to run the simulation, this software is designed to be compatible with the [ROS Noetic](http://wiki.ros.org/noetic) environment. To ensure smooth execution, it is necessary to have a properly initialized ROS workspace. Additionally, there are several required packages that need to be installed to support the functionality of the software
  - [roslaunch](http://wiki.ros.org/roslaunch), to launch the files in the package.
  - [rospy](http://wiki.ros.org/rospy), to use python with ROS.
  - [xterm](https://wiki.archlinux.org/title/Xterm), a terminal simulator, which can be installed by running from the terminal `sudo apt install -y xterm`.
  - [ARMOR Server](https://github.com/EmaroLab/armor), is a ROS integration facilitates the manipulation of OWL ontologies online.
  - [smach](http://wiki.ros.org/smach), To enable simulation of the robot's behavior, a state machine library is utilized, which can be installed by excuting this line in the terminal `sudo apt-get install ros-noetic-smach-ros`
## Installation and Running Procedure
To install and run the project, follow these steps:
1. Navigate to your workspace's src directory.
2. Clone the project repository: `git clone https://github.com/husseinfd97/as_1.git`
3. Build the project: `catkin_make`
4. Launch the project: `roslaunch as_1 project.launch`

## System's Features
The implemented system offers the following key features:
- Ability to load the topological map and establish relations between locations and doors.
- Navigation logic based on the surveillance policy, prioritizing corridors and visiting rooms.
- Battery monitoring and recharging functionality.

## System's Limitations
While the implemented system covers the specified requirements, it also has some limitations:
- The surveillance policy is simple and does not consider dynamic changes or complex decision-making.
- The environment is limited to a predefined 2D layout with a fixed number of rooms and corridors.
- The system does not incorporate any external sensing or perception capabilities.

## Possible Technical Improvements
To enhance the system, the following improvements can be considered:
- Implementing more sophisticated surveillance policies that account for dynamic factors and optimize robot movement.
- Extending the environment to support a larger number of rooms, corridors, and door configurations.
- Integrating additional sensors and perception capabilities to enable more advanced navigation and mapping functionalities.

By addressing these improvements, the system can be further optimized for various real-world scenarios and requirements.

***Author***: Hussein Ahmed Fouad Hassan

***Email***: S5165612@studenti.unige.it

