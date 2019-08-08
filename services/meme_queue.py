# -*- coding: utf-8 -*-
import asyncio


__all__ = ["AsyncQueue"]


class AsyncQueue(asyncio.Queue):

    # @Valejnick
    SEND_POSTS_TO = 162216950  # Trush
    DISABLE_NOTIFICATION = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def start_posting(self, control, timeout=1):
        """ Get meme from queue and post it.

        :type timeout: int: time (in minutes) to sleep between next post
        """
        while 1:
            meme = await self.get()
            await control.send_photo(self.SEND_POSTS_TO, meme.file_id, disable_notification=self.DISABLE_NOTIFICATION)
            await asyncio.sleep(timeout*60)


if __name__ == '__main__':
    pass
