import requests
import json
import xml.etree.ElementTree as etree
from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern, SimpleTagPattern


SOURCE = "https://api.github.com/emojis"
EMOJI_RE = r'(:)((?:[\+\-])?[0-9a-zA-Z]*?):'


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
