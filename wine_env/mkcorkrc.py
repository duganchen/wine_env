#!/usr/bin/env python

from wine_env.wine_rc import Main, CorkRC


def main():

    main = Main(CorkRC)
    main.main()

if __name__ == '__main__':
    main()
