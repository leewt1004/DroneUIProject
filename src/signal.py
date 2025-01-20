from pymavlink import mavutil

def connect_drone():
    print("드론 연결 중...")
    connection = mavutil.mavlink_connection('udp:127.0.0.1:14551')
    connection.wait_heartbeat()
    print("드론 연결 완료!\n")
    return connection
