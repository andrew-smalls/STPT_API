import time
from updater import *


def do_every(period, function):#, *args):
    def g_tick():
        t = time.time()
        while True:
            t += period
            yield max(t - time.time(), 0)

    g = g_tick()
    while True:
        time.sleep(next(g))
        print("Calling updater")
        function()


do_every(20, updateAll)

#updateAll(verbose=False)