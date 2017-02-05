from wine_env import wine_rc
import argparse
import os
import re


def main() -> None:

    parser = argparse.ArgumentParser()
    parser.add_argument('bottle', help='The name of the Wine bottle, e.g. PvZ', type=is_valid_bottle)
    parser.add_argument('--wine', help='The path to the Wine executable to use')
    args = parser.parse_args()

    if args.wine and not os.path.isfile(args.wine):
        print('Wine must be the path to an executable')
        sys.exit(1)

    bin = os.path.join(os.path.expandvars('$HOME'), '.local', 'share', 'wineprefixes', args.bottle, 'bin')
    os.makedirs(bin, exist_ok=True)

    rcs = (
        ('runrc.sh', wine_rc.RunRC(args.bottle, args.wine),
        ('runrc.fish', wine_rc.RunRCFish(args.bottle, args.wine)),
        ('uncorkrc.sh', wine_rc.UncorkRC(args.bottle, args.wine)),
        ('uncorkrc.fish', wine_rc.UncorkRCFish(args.bottle, args.wine)),
    )

    for rc_basename, rc_maker in rcs:
        with open(os.path.join(bin, rc_basename), 'w+') as f:
            f.write(rc_maker.get_rc())

    print('Activate the bottle with:')
    print(f'\tuncork {args.bottle}')


def is_valid_bottle(value: str) -> str:
    if not re.match(r'^\w+$', value):
        raise argparse.ArgumentTypeError(f'{value} is not a valid bottle name.')
    return value
