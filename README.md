# DroneUIProject


## Project Description
DroneUIProject is a Python project that uses Tkinter to automate and control drones through a user interface (UI). This project uses pymavlink to communicate with the drone and provides the following key features
  - Drone connection and initialization
  - Drone Arm and Takeoff
  - Move Flight
  - Landing
  - Program exit


## Project Structure
DroneUIProject/  
├── src/  
│   ├── arm_takeoff.py      # Drone Arm and Takeoff functions  
│   ├── exit.py             # Program termination function  
│   ├── land_disarm.py      # Drone land and disarm functions  
│   ├── move.py             # Route flight function  
│   ├── signal.py           # Drone connection function  
├── main.py                 # Main file that integrates all functions  
└── README.md               # Project description file




## How to install and run
 1. install dependencies
   - Install the pymavlink library : pip install pymavlink  
 2. SITL execution
   - To run the drone in a simulated environment, use the following command : python3 sim_vehicle.py -v ArduCopter --out=127.0.0.1:14551
 3. Project execution
   - python3 main.py  


## How to use
 - Arm / Takeoff : Activates the drone and takes off at an altitude of 10 meters(altitude can be modified)
 - Move Flight : Move the drone along a predefined path(path can be modified)
 - Land : Land the drone
 - Exit : Terminates the program.

## Technology Stack
 - Python 3.x: The main programming language for the project
 - pymavlink: A library for drone communication
 - Tkinter: A library for creating user interfaces (UI)


## How to Contribute
If you would like to contribute to this project, please follow these steps
 - Fork this repository.
 - Create a new branch(git checkout -b feature/my-feature)
 - Modify the code and commit : git commit -m "Add my feature"  
 - Create a Pull Request


## license
This project is licensed under the MIT License. For more information, see LICENSE