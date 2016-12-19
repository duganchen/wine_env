#!/usr/bin/env python

from __future__ import (
    division, absolute_import, print_function, unicode_literals
)

from wine_env.wine_rc import Main, CorkRCFish


def main():

    main = Main(CorkRCFish)
    main.main()

if __name__ == '__main__':
    main()
