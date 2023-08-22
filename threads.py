import threading
from time import sleep

def user_interface():
    while True:
        sleep(0.2)
        print("-", end="")


def task():
    while True:
        sleep(0.61)
        print("*", end="")

threading.Thread(target=user_interface())
threading.Thread(target=task())
