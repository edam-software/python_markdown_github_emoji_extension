#!/usr/bin/env python3.10

import aiohttp
import requests
import json
from pathlib import Path
from markdown.inlinepatterns import InlineProcessor
import xml.etree.ElementTree as etree
from markdown.extensions import Extension


SOURCE = "https://api.github.com/emojis"

# let there be +1
EMOJI_RE = r'(:)((?:[\+\-])?[_0-9a-zA-Z]*?):'

# download is not required to use, just for fun
SAVE_PATH = "./python_markdown_github_emoji_extension/files/"


class GheEmoji(Extension):

    def __init__(self, **kwargs):
        self.config = {
            'emoji': [{}, 'Dict emojiname : url ']
        }
        super(GheEmoji, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        pattern = EmojiInlineProcessor(EMOJI_RE, self.getConfig('emoji'))
        # Insert del pattern into markdown parser
        md.inlinePatterns.register(pattern, 'emoji', 100)

    @staticmethod
    def load_from_github():
        try:
            resp = requests.get(SOURCE)
            payload = resp.content
            data = json.loads((payload.decode('utf-8')))
            return GheEmoji(emoji=data)
        except Exception as e:
            print(e)

    @staticmethod
    async def get_bytes(url: str) -> bytes:
        async with aiohttp.ClientSession() as sesh:
            async with sesh.get(url) as payload:
                data = await payload.read()
                print(f"Finished downloading {url}")
                return data

    @staticmethod
    async def write_bytes(path: str, data: bytes) -> bool:
        try:
            with Path(f"{SAVE_PATH}{path}.png").open('xb') as file_name:
                file_name.write(data)
                print(f"Finished writing {path}")
        except FileExistsError as failed:
            print(failed)
            return

    @staticmethod
    async def fetch_task(tag: str, url: str):
        file = url.split('/')[-1]
        content = await GheEmoji.get_bytes(url)
        await GheEmoji.write_bytes(tag, content)

    async def download(self):
        tasks = []
        for tag, url in self.getConfig('emoji').items():
            tasks.append(self.fetch_task(tag, url))
        await asyncio.wait(tasks)


class EmojiInlineProcessor(InlineProcessor):
    def __init__(self, pattern, emoji):
        super(EmojiInlineProcessor, self).__init__(pattern)
        self.emoji = emoji

    def handleMatch(self, m, data):
        tag = m.group(2)
        url = self.emoji.get(tag, '')
        if not url:
            return None, None, None
        el = etree.Element("img")
        el.set("src", url)
        el.set("title", tag)
        el.set("alt", tag)
        return el, m.start(0), m.end(0)


if __name__ == '__main__':
    print("This is an extension to Markdown please import it.")
