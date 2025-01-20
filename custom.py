from pymavlink import mavutil
import time
import math

# UDP port 연결
drone_connection = mavutil.mavlink_connection('udp:127.0.0.1:14551')

# Heartbeat 수신 대기
print("Listening to Heartbeat")
drone_connection.wait_heartbeat()
print("Heartbeat received (system %u component %u)"%
    (drone_connection.target_system, drone_connection.target_component))


# Arm / Take off 함수
def arm_takeoff() :
    print("Arming")
    drone_connection.mav.command_long_send(
        drone_connection.target_system,
        drone_connection.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0, 1, 0, 0, 0, 0, 0, 0
    )

    message = drone_connection.recv_match(type = 'COMMAND_ACK', blocking = True)
    print(f"Arming : {message}")

    print("Change GUIDED MODE")
    drone_connection.mav.command_long_send(
        drone_connection.target_system,
        drone_connection.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE,
        0, 1, 4, 0, 0, 0, 0, 0
    )

    message = drone_connection.recv_match(type = 'COMMAND_ACK', blocking = True)
    print("GUIDED MODE change completed")

    print("TAKE OFF")
    drone_connection.mav.command_long_send(
        drone_connection.target_system,
        drone_connection.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0, 0, 0, 0, 0, 0, 0, 10
    )

    message = drone_connection.recv_match(type = 'COMMAND_ACK', blocking = True)
    print(f"TAKE OFF : {message}")

    drone_altitude = 10 # 목표고도(단위 : 미터)
    while True :
        message = drone_connection.recv_match(type = 'GLOBAL_POSITION_INT', blocking = True)
        if not message : 
            continue
        current_altitude = message.relative_alt / 1000.0
        print(f"current altitude : {current_altitude:.2f}m")
        if current_altitude >= drone_altitude : 
            print("TAKE OFF Success")
            print("Target altitude reached")
            break
        time.sleep(0.5)

# 목표지점 이동명령 및 속도설정 함수
def move(x, y, z) : 
    drone_connection.mav.command_long_send( # 목표지점 이동 전 속도 20m/s 설정
        drone_connection.target_system,
        drone_connection.target_component,
        mavutil.mavlink.MAV_CMD_DO_CHANGE_SPEED,
        1,  # 속도유형(groundspeed)
        20, # 속도(m/s)
        -1, 0, 0, 0, 0, 0
    )
    print("The set speed is 20m/s")

    drone_connection.mav.send(
        mavutil.mavlink.MAVLink_set_position_target_local_ned_message(
            10,
            drone_connection.target_system,
            drone_connection.target_component,
            mavutil.mavlink.MAV_FRAME_LOCAL_NED,
            int(0b110111111000),
            x, y, z, 0, 0, 0, 0, 0, 0, 0, 0
        )
    )

    last_position = None
    last_time = time.time()

    while True :
        message = drone_connection.recv_match(type = 'LOCAL_POSITION_NED', blocking = True)
        if not message : 
            continue

        current_position = (message.x, message.y, message.z)
        current_time = time.time()

        print(f"Current location - X: {message.x:.2f}, Y: {message.y:.2f}, Z: {message.z:.2f}")

        if last_position :
            distance = math.sqrt(
                (current_position[0] - last_position[0]) ** 2 +
                (current_position[1] - last_position[1]) ** 2 +
                (current_position[2] - last_position[2]) ** 2
            )
            time_diff = current_time - last_time
            if time_diff > 0 :
                speed = distance / time_diff
                print(f"Current speed : {speed:.2f}m/s")

        last_position = current_position
        last_time = current_time

        if math.isclose(message.x, x, abs_tol=1) and math.isclose(message.y, y, abs_tol=1):
            print("Reached the target point")
            break
        time.sleep(0.5)

# 경로비행 함수
def move_flight():
    print("경로 비행을 시작합니다")
    waypoints = [
        (50, 0, -10),   # 북쪽으로 50m
        (50, 20, -10),  # 동쪽으로 20m
        (0, 20, -10),   # 남쪽으로 50m
        (0, 40, -10),   # 동쪽으로 20m

        (50, 40, -10),  # 북쪽으로 50m
        (50, 60, -10),  # 동쪽으로 20m
        (0, 60, -10),   # 남쪽으로 50m
        (0, 80, -10),   # 동쪽으로 20m

        (50, 80, -10),  # 북쪽으로 50m
        (50, 100, -10), # 동쪽으로 20m
        (0, 100, -10),  # 남쪽으로 50m
        (0, 0, -10)     # 서쪽으로 100m
    ]
    for waypoint in waypoints:
        move(*waypoint)

    print("Route flight is complete")

# 착륙 함수
def land() :
    print("Landing")
    drone_connection.mav.command_long_send(
        drone_connection.target_system,
        drone_connection.target_component,
        mavutil.mavlink.MAV_CMD_NAV_LAND,
        0, 0, 0, 0, 0, 0, 0, 0
    )

    while True :
        message = drone_connection.recv_match(type = 'GLOBAL_POSITION_INT', blocking = True)
        if not message :
            continue
        current_altitude = message.relative_alt / 1000.0
        print(f"Current altitude : {current_altitude:.2f}m")
        if current_altitude <= 0.1 :    # 지면 근처
            print("Landing OK")
            break
        time.sleep(0.5)

# Disarm 함수
def disarm() :
    print("Disarming")
    drone_connection.mav.command_long_send(
    drone_connection.target_system,
    drone_connection.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0, 0, 0, 0, 0, 0, 0, 0
    )
    message = drone_connection.recv_match(type = 'COMMAND_ACK', blocking = True)
    print(f"Disarm : {message}")
    if message and message.result == 0 :    # MAV_RESULT_ACCEPTED
        print("Disarm OK")

# 키보드 입력 메인루프
while True : 
    print("\n Command Button : ")
    print("Button 1 = Arm / Take off")
    print("Button 2 = Move")
    print("Button 3 = Land")
    print("Button 4 = Disarm")
    print("Button 0 = Finish")

    command = input("Please press the command button")

    if command == '1' : 
        arm_takeoff()
    elif command == '2' :
        move_flight()
    elif command == '3' :
        land()
    elif command == '4' :
        disarm()
    elif command == '0' :
        print("Shut down the system")
        break
    else :
        print("This is an invalid command. Please enter the correct command ")
