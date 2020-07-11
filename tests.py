import markdown
from ghe_emoji import GheEmoji


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

