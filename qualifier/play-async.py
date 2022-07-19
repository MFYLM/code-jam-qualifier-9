from multiprocessing import Process
import asyncio
import time


'''
async acts like a wrapper around function object and transfer it into a coroutine object, which needs to be awaited before running

in python, in order to run asynchronous program, we need to define a asyn event-loop

await keyword can only be used in a function which is defined by async keyword


create_task allows us to create a task and let rest of the code running until it takes a break(return keyword) or done(end of file) rest of code

await task --> this line will force python to execute rest of code after hearing from task

await asynchio.sleep(num_in_sec)  --> this function force execution of current function and give resource to other functions (can't let processor doing nothing)


more than one asyncio.run() will run task in the same time?

future (like promise in JavaScript) to get return value from task --> value will be returned in the future
'''







async def A(a: int):
    print("inside function A")
    await asyncio.sleep(10)
    task = asyncio.create_task(f(a))
    #await task
    print("finishing function A")
    return task

async def f(b: int):
    await asyncio.sleep(2)
    print("we are in f")
    return b * 2


async def main():
    time1 = time.time()

    # in here , tasks actually have already started, but we need to await tasks in order to let them finish
    task1 = asyncio.create_task(f(2))
    task2 = asyncio.create_task(A(2))

    print("result of function f:", await task1)
    print("-------------------------")
    print("result of function A:", await task2)

    # we could await multiple tasks in the same time

    time2 = time.time()
    print(f"Finished in {time2 - time1}s")

if __name__ == "__main__":
    asyncio.run(main())     # idealy, asyncio.run() should only call once and is the entry point of a async program
