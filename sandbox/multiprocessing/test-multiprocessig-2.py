__author__ = 'marion'

from sandbox.multiprocessing import Process, Queue

def f(q, i):
    q.put([42, None, 'hello' + str(i)])
    while True:
        pass

if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,0))
    p.start()
    print q.get()    # prints "[42, None, 'hello']"
    p.join()

