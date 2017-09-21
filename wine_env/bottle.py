from wine_env import wine_rc
import argparse
import os
import re
import sys


def main() -> None:

    parser = argparse.ArgumentParser()
    parser.add_argument('bottle', help='The name of the Wine bottle, e.g. PvZ', type=is_valid_bottle)
    parser.add_argument('--wine', help='The path to the Wine executable to use')
    parser.add_argument('--winearch', help='Set WINEARCH to this value')
    args = parser.parse_args()

    if args.wine and not os.path.isfile(args.wine):
        print('Wine must be the path to an executable')
        sys.exit(1)

    bin = os.path.join(os.path.expandvars('$HOME'), '.config', 'wine_env', args.bottle)
    os.makedirs(bin, exist_ok=True)

    rcs = (
        ('runrc.sh', wine_rc.RunRC(args.bottle, args.wine, args.winearch)),
        ('runrc.fish', wine_rc.RunRCFish(args.bottle, args.wine, args.winearch)),
        ('uncorkrc.sh', wine_rc.UncorkRC(args.bottle, args.wine, args.winearch)),
        ('uncorkrc.fish', wine_rc.UncorkRCFish(args.bottle, args.wine, args.winearch)),
    )

    for rc_basename, rc_maker in rcs:
        with open(os.path.join(bin, rc_basename), 'w+') as f:
            f.write(rc_maker.get_rc())

    print('Activate the bottle with:')
    print(f'\tuncork {args.bottle}')
    print('Then create it on disk with:')
    print(f'\twinecfg')
    print('And go to its C: drive:')
    print(f'\tgoc')
    print()
    print('To delete the bottle, remove the following directories:')
    print(f'\t{bin}')
    prefix = os.path.expandvars(f'$HOME/.local/share/wineprefixes/{args.bottle}')
    print(f'\t{prefix}')


def is_valid_bottle(value: str) -> str:
    if not re.match(r'^\w+$', value):
        raise argparse.ArgumentTypeError(f'{value} is not a valid bottle name.')
    return value
