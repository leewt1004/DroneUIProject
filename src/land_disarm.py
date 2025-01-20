from pymavlink import mavutil
import time

def land_drone(connection):
    print("Landing 시작")
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_NAV_LAND,
        0, 0, 0, 0, 0, 0, 0, 0
    )

    while True:
        msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        if not msg:
            continue
        current_altitude = msg.relative_alt / 1000.0
        print(f"현재 고도: {current_altitude:.2f}m")
        if current_altitude <= 0.1:  # 지면 근처
            print("Landing 완료!")
            print("Disarming 완료!\n")  # 착륙 후 Disarm 상태 알림
            break
        time.sleep(0.5)
