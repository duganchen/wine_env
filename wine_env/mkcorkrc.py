#!/usr/bin/env python3

from wine_env.wine_rc import Main, CorkRC


def main():

    main = Main(CorkRC)
    main.main()

if __name__ == '__main__':
    main()
