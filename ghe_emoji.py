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
    def fetch_tag(tag, url):
        file = url.split('/')[-1]
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            try:
                with open(Path(f"{SAVE_PATH}{tag}.png"), 'xb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        # If you have chunk encoded response uncomment if
                        # and set chunk_size parameter to None.
                        # if chunk:
                        f.write(chunk)
            except FileExistsError as failed:
                print(failed)
                return

    def download(self):
        for tag, url in self.getConfig('emoji').items():
            try:
                self.fetch_tag(tag, url)
            except requests.exceptions.HTTPError as notfound:
                print(notfound)
                continue


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
    print("This is an extension to Markdown please import it")
