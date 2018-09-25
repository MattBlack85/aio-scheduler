# aio-scheduler [![Build Status](https://travis-ci.org/MattBlack85/aio-scheduler.svg?branch=master)](https://travis-ci.org/MattBlack85/aio-scheduler)

Small library that want to be lightweight and offload coroutine scheduling to another thread running its own event loop.

## Motivation
asyncio does not have a built-in way of building periodic tasks, the usual way is to have a coroutine running a while true loop:
```Python
async def my_coro():
    while True:
        ...do_stuff...
        asyncio.sleep(X)
```
this way the coroutine will do stuff every X seconds.
This is not really a nice option cause the coroutine itself won't return, never, and closing loops become a bit more
complicated.
Also IMO a coroutine's scope should not be to related to do some job every X time, but just doing some job, period.
If we want to do that job periodically somebody else should schedule it, that's where this scheduler chime in.

## Usage
The scheduler is a thread running its own event loop
```Python
from aioscheduler import AsyncIOScheduler

scheduler = AsyncIOScheduler()
# Start the thread
scheduler.start()
```

calling `.start()` won't actually do nothing, in fact the scheduler is waiting with a blocking call for some tasks
to be added.
If you want to add a periodic task just call:
```Python
scheduler.add_periodic('task_name', coro, 1, event_loop)
```
Note that the event loop passed to the scheduler for a given periodic task is the event loop
where the task will be scheduled to run periodically, not the scheduler event loop, this is possible
thanks to the `asyncio.run_coroutine_threadsafe()` method

When add_periodic is call the thread starts its event loop and will try to dispatch periodically the task at given `interval`
on the given event loop.

Before trying to scheduler a coroutine, the scheduler checks if the coroutine's event loop is still opened, if not the task is removed
from the list of periodic tasks.
If there is no more periodc tasks to be scheduled the scheduler will block again (and not consuming CPU) and will wait for some more work
to come again.
