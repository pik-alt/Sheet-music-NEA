fib = [0,1]
import time

start = time.time()

while time.time() - start < 0.001:
    newfib = fib[0] + fib[1]

    fib[0] = fib[1]
    fib[1] = newfib

print(len(str(fib[1])))