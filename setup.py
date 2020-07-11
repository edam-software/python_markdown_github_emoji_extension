try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


setup(
    name='ghe_emoji',
    version='0.5',
    packages=find_packages(),
    py_modules=['ghe_emoji'],
    install_requires=['markdown>=3.0', 'requests'],
    python_requires='>3.7',
    url='https://github.com/edam-software/github_emojis',
    license="OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    author='EDAM',
    author_email='eric.arellano@hey.com',
    description='Markdown extension to provide Github emoji (in Pelican)',
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent"]
)

