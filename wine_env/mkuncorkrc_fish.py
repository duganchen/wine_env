#!/usr/bin/env python

from __future__ import (
    division, absolute_import, print_function, unicode_literals
)

from wine_env.wine_rc import Main, UncorkRCFish

def main():

    main = Main(UncorkRCFish)
    main.main()

if __name__ == '__main__':
    main()
