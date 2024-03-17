import time

def funct():
    for _ in range(1, 100):
        print("logging :: >>>>>>>>>>>>>>>>>>>>>>>>>>")
        time.sleep(5)
        print("printing :: >>>>>>>>>>>>>>>>>>>>>>>>>>")

if __name__ == '__main__':
    funct()
