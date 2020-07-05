from setuptools import setup

setup(
    name='github_emoji',
    version='0.2',
    packages=[''],
    py_modules=['EmojiExtension'],
    install_requires=['markdown>=3.0', 'requests'],
    url='https://github.com/edam-software/github_emojis',
    license='GPL v3',
    author='EDAM',
    author_email='eric.arellano@hey.com',
    description='Markdown extension to provide Github emoji in Pelican'
)
