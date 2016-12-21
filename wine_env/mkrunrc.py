#!/usr/bin/env python3

from wine_env.wine_rc import Main, RunRC


def main():

    main = Main(RunRC)
    main.main()

if __name__ == '__main__':
    main()
