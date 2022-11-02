import asyncio
class MessageAnnouncer:#questa classe pemette di comunicare tra due endpoint

    def __init__(self):
        self.listeners = []

    async def listen(self):
        self.listeners.append(asyncio.Queue(maxsize=1))
        return self.listeners[-1]

    async def announce(self, msg):
        # We go in reverse order because we might have to delete an element, which will shift the
        # indices backward
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except asyncio.QueueFull:
                del self.listeners[i]

announcer = MessageAnnouncer()