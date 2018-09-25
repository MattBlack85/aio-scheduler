import asyncio
import threading

work_available = threading.Event()


class AsyncIOScheduler(threading.Thread):
    """
    Register functions to be executed periodically and dispatch them to
    an event loop
    """
    daemon = True

    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self._periodic_tasks = {}
        super().__init__()

    def add_periodic(self, name: str, func, interval: float, loop: asyncio.BaseEventLoop):
        """
        Add a task to be dispatched to an event loop periodically, after that signal that we
        have some work to do and the thread event loop can start
        """
        self._periodic_tasks[name] = {
            'func': func,
            'interval': interval,
            'loop': loop,
            'last_executed': self.loop.time()
        }
        if not work_available.is_set():
            work_available.set()

    @property
    async def periodic_tasks(self):
        for name, task in self._periodic_tasks.items():
            yield name, task

    def remove_periodic(self, name: str):
        try:
            del self._periodic_tasks[name]
        except KeyError:
            pass

    def remove_all_tasks(self):
        self._periodic_tasks = {}
        work_available.clear()

    async def start_schedule(self):
        """
        The scheduler, every time the event loop leave this coroutine space to run
        check if there is any task that can be dispacthed (checking last time task
        has been executed vs. the actual loop time.
        """
        while True:
            now = self.loop.time()
            if self.periodic_tasks:
                async for task_name, task in self.periodic_tasks:
                    if task['loop'].is_closed():
                        self.remove_periodic(task_name)
                    else:
                        if now - task['last_executed'] >= task['interval']:
                            asyncio.run_coroutine_threadsafe(task['func'](), task['loop'])
                            task['last_executed'] = self.loop.time()

                await asyncio.sleep(0)
            else:
                work_available.clear()
                break

    def run(self):
        """
        Thread entry point, lock until somebody adds some task to be dispatched, then
        start the event loop and dispatch tasks accordingly to the task spec itself.
        """
        while True:
            work_available.wait()
            self.loop.run_until_complete(self.start_schedule())

    def stop(self):
        self.remove_all_tasks()
