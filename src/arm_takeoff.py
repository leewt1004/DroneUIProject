from pymavlink import mavutil
import time

def arm_and_takeoff(connection, target_altitude=10):
    print("Arming 드론")
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0, 1, 0, 0, 0, 0, 0, 0
    )
    msg = connection.recv_match(type='COMMAND_ACK', blocking=True)
    if msg and msg.result == 0:
        print("Arming 성공\n")
    else:
        print(f"Arming 실패: {msg}")
        return

    print("GUIDED Mode로 변경 중")
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE,
        0, 1, 4, 0, 0, 0, 0, 0
    )
    msg = connection.recv_match(type='COMMAND_ACK', blocking=True)
    if msg and msg.result == 0:
        print("GUIDED Mode 변경 성공\n")
    else:
        print(f"GUIDED Mode 변경 실패: {msg}")
        return

    print("Take off 명령 전송")
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0, 0, 0, 0, 0, 0, 0, target_altitude
    )
    msg = connection.recv_match(type='COMMAND_ACK', blocking=True)
    if msg and msg.result == 0:
        print("Take off 명령 수락\n")
    else:
        print(f"Take off 명령 실패: {msg}")
        return

    print(f"목표 고도 {target_altitude}m로 상승 중...")
    while True:
        msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        if not msg:
            continue
        current_altitude = msg.relative_alt / 1000.0
        print(f"현재 고도: {current_altitude:.2f}m")
        if current_altitude >= target_altitude * 0.95:
            print("Take off 성공!\n")
            break
        time.sleep(0.5)
