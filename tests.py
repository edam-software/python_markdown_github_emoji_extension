import markdown
from ghe_emoji import GheEmoji
from datetime import datetime
import asyncio


t0 = datetime.now()
m = GheEmoji.load_from_github()
print(f"The time is now: {t0}")
asyncio.run(m.download())
dt = datetime.now() - t0
print(f"This took {dt} to run")

txt = """
 line 1 :fight:
 line 2 :smiley:
 line 3 :metal:
 """

result = markdown.markdown(txt, extensions=[GheEmoji.load_from_github()])
assert result == """<p>line 1 
 line 2 <img alt="smiley" src="https://github.githubassets.com/images/icons/emoji/unicode/1f603.png?v8" title="smiley" />
 line 3 <img alt="metal" src="https://github.githubassets.com/images/icons/emoji/unicode/1f918.png?v8" title="metal" /></p>"""

# plus_one = """
# :+1: the plus sign
# """
#
# thumbs_up = markdown.markdown(plus_one, extensions=[GheEmoji.load_from_github()])
# print(thumbs_up)
