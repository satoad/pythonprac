import asyncio

event = asyncio.Event()

async def writer(queue, time):
    counter = 0
    while not event.is_set():
        await asyncio.sleep(time)
        await queue.put(str(counter) + '_' + str(time))
        counter += 1

async def stacker(queue, stack):
    while not event.is_set():
        await stack.put(await queue.get())

async def reader(stack, count, time):
    for _ in range(count):
        await asyncio.sleep(time)
        print(await stack.get())
    event.set()

async def main():
    queue = asyncio.Queue()
    stack = asyncio.Queue()

    t1, t2, t3, count = eval(input())

    await asyncio.gather(
        writer(queue, t1),
        writer(queue, t2),
        stacker(queue, stack),
        reader(stack, count, t3))

asyncio.run(main())