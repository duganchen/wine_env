#!/usr/bin/env python

from __future__ import (
    division, absolute_import, print_function, unicode_literals
)

from wine_env.wine_rc import Main, UncorkRC

def main():

    main = Main(UncorkRC)
    main.main()

if __name__ == '__main__':
    main()
