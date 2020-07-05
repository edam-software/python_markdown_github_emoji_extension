from setuptools import setup

setup(
    name='github_emoji',
    version='0.5',
    packages=[''],
    py_modules=['GheEmoji'],
    install_requires=['markdown>=3.0', 'requests'],
    url='https://github.com/edam-software/github_emojis',
    license='GPL v3',
    author='EDAM',
    author_email='eric.arellano@hey.com',
    description='Markdown extension to provide Github emoji (in Pelican)'
)
