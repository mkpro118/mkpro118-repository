import concurrent.futures
import os
import time

def func(drive):
    T1 = time.perf_counter()
    ctr = 0
    print(f'Started counting {drive} drive\n')
    dirname = os.path.dirname(f'{drive}:\\')
    for roots, dirs, files in os.walk(dirname):
        for file in files:
            ctr += 1
    return f'{ctr} files in drive {drive} (took {round(time.perf_counter()-T1,2)} seconds)\n'


print('attempt threaded\n'.upper())
t1 = time.perf_counter()
drives = ['D','C']
with concurrent.futures.ThreadPoolExecutor() as executor:
    results = [executor.submit(func, drive) for drive in drives]

    for result in concurrent.futures.as_completed(results):
        print(result.result())  

print('total time taken: ', round((time.perf_counter() - t1), 2), ' seconds')
print()

time.sleep(1)

print('-'*35,'\n')
print('attempt unthreaded\n'.upper())
t1 = time.perf_counter()
print(func('D'))
print(func('C'))

print('total time taken: ', round((time.perf_counter() - t1), 2), ' seconds')


#output
'''ATTEMPT THREADED

Started counting D drive

Started counting C drive

160527 files in drive D (took 11.87 seconds)

428116 files in drive C (took 44.26 seconds)

total time taken:  44.27  seconds

----------------------------------- 

ATTEMPT UNTHREADED

Started counting D drive

160527 files in drive D (took 8.82 seconds)

Started counting C drive

428120 files in drive C (took 42.44 seconds)

total time taken:  51.26  seconds'''