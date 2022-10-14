
#!/usr/bin/python3
from setuptools import setup
import io
import os

# Package meta-data
NAME = 'twdl'

# Packages required
REQUIRED = [
    'aiohttp', 'aiodns', 'beautifulsoup4', 'cchardet', 'dataclasses',
    'schedule', 'fake-useragent'
]

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

about = {}
with open(os.path.join(here, NAME, '__version__.py')) as f:
    exec(f.read(), about)

setup(
    name=NAME,
    version="0.0.5",
    packages=['twdl', 'twdl.storage'],
    entry_points={
        'console_scripts': [
            'twdl = twdl.cli:run_as_command',
        ],
    },
    dependency_links=[],
    license='MIT'
)
