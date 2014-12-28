#!/usr/bin/env python

from wine_env.wine_rc import Main, RunRC


def main():

    main = Main(RunRC)
    main.main()

if __name__ == '__main__':
    main()
