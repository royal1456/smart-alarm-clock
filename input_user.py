import threading
import time
import keyboard
user_input = [None]

# spawn a new thread to wait for input
def get_user_input(user_input_ref):
    user_input_ref[0] = input("Give me some Information: ")
while True:
    mythread = threading.Thread(target=get_user_input, args=(user_input,))
    mythread.daemon = True
    mythread.start()
    for increment in range(1, 10):
        time.sleep(1)
        if user_input[0] is not None:
            break
    keyboard.write("Skipped")