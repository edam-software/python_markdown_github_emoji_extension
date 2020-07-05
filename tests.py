import pytest
import markdown
from github_emojis import GheEmoji

txt = """
 line 1 :fight:
 line 2 :smiley:
 line 3 :metal:
 """
print(markdown.markdown(txt, extensions=[GheEmoji.load_from_github()]))


