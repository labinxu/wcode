import asyncio
import time
now = lambda:time.time()

async def do_some_work(x):
    print('Waiting: ',x)
    await asyncio.sleep(x)
    return 'Done after {}s'.format(x)

async def main():
    c1 = do_some_work(1)
    c2 = do_some_work(2)
    c3 = do_some_work(4)
    tasks = [
        asyncio.ensure_future(c1),
        asyncio.ensure_future(c2),
        asyncio.ensure_future(c3),
    ]

    if None:
        dones, pendings = await asyncio.wait(tasks)
        for t in dones:
            print('Task ret:', t.result())
    else:
        return await asyncio.wait(tasks)

start = now()
loop = asyncio.get_event_loop()
if not None:
    dones, pending = loop.run_until_complete(main())
    for task in dones:
            print('Task ret:', task.result())

print('TIME: ',now()-start)
