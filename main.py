from src.signal import connect_drone
from src.arm_takeoff import arm_and_takeoff
from src.move import move_flight
from src.land_disarm import land_drone
from src.exit import exit_program
import tkinter as tk

# 드론 연결
connection = connect_drone()

# Tkinter UI 생성
root = tk.Tk()
root.title("Drone Control Panel")
root.geometry("300x280")

# 버튼 생성
btn_arm_takeoff = tk.Button(root, text="Arm / Take Off", command=lambda: arm_and_takeoff(connection), height=2, width=20)
btn_move_flight = tk.Button(root, text="Move Flight", command=lambda: move_flight(connection), height=2, width=20)
btn_land = tk.Button(root, text="Land / Disarm", command=lambda: land_drone(connection), height=2, width=20)
btn_exit = tk.Button(root, text="Exit", command=lambda: exit_program(connection, root), height=2, width=20)

# 버튼 배치
btn_arm_takeoff.pack(pady=10)
btn_move_flight.pack(pady=10)
btn_land.pack(pady=10)
btn_exit.pack(pady=10)

# Tkinter 이벤트 루프 실행
root.mainloop()
