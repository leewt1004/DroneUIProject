def exit_program(connection, root):
    print("프로그램 종료 중...")
    try:
        connection.close()
        print("드론 연결이 안전하게 종료되었습니다.")
    except Exception as e:
        print(f"드론 연결 종료 중 오류 발생: {e}")
    root.destroy()
