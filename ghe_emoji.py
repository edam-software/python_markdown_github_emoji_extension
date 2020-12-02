#!/bin/env python3

import aiohttp
import asyncio
import requests
import json
import xml.etree.ElementTree as etree
from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern, SimpleTagPattern
from pathlib import Path

SOURCE = "https://api.github.com/emojis"
EMOJI_RE = r'(:)((?:[\+\-])?[_0-9a-zA-Z]*?):'
SAVE_PATH = "/Users/airbook/PycharmProjects/pelican_github_emoji/files/"


class GheEmoji(Extension):

    def __init__(self, **kwargs):
        self.config = {
            'emoji': [{}, 'Dict emojiname : url ']
        }
        super(GheEmoji, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        pattern = EmojiInlinePattern(EMOJI_RE, self.getConfig('emoji'))
        # Insert del pattern into markdown parser
        md.inlinePatterns.add('emoji', pattern, '>not_strong')

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


class EmojiInlinePattern(Pattern):
    def __init__(self, pattern, emoji):
        super(EmojiInlinePattern, self).__init__(pattern)
        self.emoji = emoji

    def handleMatch(self, m):
        tag = m.group(3)
        url = self.emoji.get(tag, '')
        if not url:
            return ""
        el = etree.Element("img")
        el.set("src", url)
        el.set("title", tag)
        el.set("alt", tag)
        return el


if __name__ == '__main__':
    print("This is an extension to Markdown please import it to retrieve icon URLs")
