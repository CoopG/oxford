import os

from oxford_client import OxfordClient


class Args:
    def __init__(self, *args):
        for arg in args:
            setattr(self, arg, os.getenv(arg, ''))


args = Args('entry', 'lexicalCategory')


ox = OxfordClient()

if args.entry:
    e = ox.entry
    response = e(args.entry)
