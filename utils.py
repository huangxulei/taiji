from threading import Thread
import time


def one_shot_thread(func, timeout=0.0):
    def run(func, timeout):
        time.sleep(timeout)
        try:
            func()
        except Exception as e:
            print(f"one_shot_thread:{func} {e}")

    Thread(target=run, args=(func, timeout), daemon=True).start()


Threads = []