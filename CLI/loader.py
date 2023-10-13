from tqdm import tqdm
import asyncio

class Loader:
    def __init__(self, timeout, prefix, call):
        self.start_value = 30
        self.total = 100
        self.bar_initial = tqdm(total=self.total, desc=prefix)
        self.timeout = timeout
        self.call = call

    async def start(self):
        total_initial = self.start_value
        for _ in range(total_initial):
            await asyncio.sleep(self.timeout / self.total)
            self.bar_initial.update(1)
        
        await self.finish()

    async def finish(self):
        self.call()

        self.bar_initial.clear()
        for _ in range(self.start_value, self.total):
            await asyncio.sleep(self.timeout / self.total)
            self.bar_initial.update(1)
        self.bar_initial.close()

class Subscriber:

    def __init__(self):
        self.subs = {}

    async def add(self, timeout, prefix, call):
        self.subs[prefix] = Loader(timeout, prefix, call)
        await self.subs[prefix].start()

    
SubscriberSingleton = Subscriber()