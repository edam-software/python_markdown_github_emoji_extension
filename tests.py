import markdown
from github_emoji import GheEmoji

txt = """
 line 1 :fight:
 line 2 :smiley:
 line 3 :metal:
 """

result = markdown.markdown(txt, extensions=[GheEmoji.load_from_github()])
assert result == """<p>line 1 
 line 2 <img alt="smiley" src="https://github.githubassets.com/images/icons/emoji/unicode/1f603.png?v8" title="smiley" />
 line 3 <img alt="metal" src="https://github.githubassets.com/images/icons/emoji/unicode/1f918.png?v8" title="metal" /></p>"""

something = """
:+1: the plus sign
"""

print_something = markdown.markdown(something, extensions=[GheEmoji.load_from_github()])
print(print_something)

