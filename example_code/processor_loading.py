
import multiprocessing
import math

def worker():
    #worker function
    print ('Worker')
    x = 0
    while x < 1000000000000000000:

        print(x)
        p = x*math.pi
        p2 = math.sqrt(x**2 + p**2)
        print(p2)

        x += 1
    return



if __name__ == '__main__':
    jobs = []

    for i in range(50):
        p = multiprocessing.Process(target=worker)
        jobs.append(p)
        p.start()