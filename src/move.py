from pymavlink import mavutil
import time
import math

def move_flight(connection):
    print("경로 비행을 시작합니다")
    # 사용자 제공 경로
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
        (0, 100, -10),  # 남쪽으로 70m
        (0, 0, -10)     # 서쪽으로 140m
    ]

    for waypoint in waypoints:
        x, y, z = waypoint
        print(f"목표 좌표로 이동 중: X={x}, Y={y}, Z={z}")
        connection.mav.send(
            mavutil.mavlink.MAVLink_set_position_target_local_ned_message(
                10,
                connection.target_system,
                connection.target_component,
                mavutil.mavlink.MAV_FRAME_LOCAL_NED,
                int(0b110111111000),  # X, Y, Z 위치 활성화
                x, y, z, 0, 0, 0, 0, 0, 0, 0, 0
            )
        )
        # 목표 지점 도달 확인
        while True:
            msg = connection.recv_match(type='LOCAL_POSITION_NED', blocking=True)
            if not msg:
                continue

            # 현재 좌표와 목표 좌표 비교
            current_x = msg.x
            current_y = msg.y
            current_z = msg.z

            print(f"현재 위치: X={current_x:.2f}, Y={current_y:.2f}, Z={current_z:.2f}")
            distance = math.sqrt((current_x - x)**2 + (current_y - y)**2 + (current_z - z)**2)

            if distance < 1.0:  # 1m 이내에 도달하면 다음 좌표로 이동
                print(f"목표 좌표 도달: X={x}, Y={y}, Z={z}\n")
                break

            time.sleep(0.5)

    print("경로 비행 완료!\n")
