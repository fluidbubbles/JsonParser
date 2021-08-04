import json
import sys
import logging
from argparse import ArgumentParser
from .constants import USAGE_MESSAGE, PARAM_HELP_MESSAGE
from nest.json_parser import JsonParser

err_handler = logging.StreamHandler(sys.stderr)
err_handler.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.addHandler(err_handler)


def run_cli():
    parser = ArgumentParser()
    parser.usage = USAGE_MESSAGE
    parser.add_argument('file', help=PARAM_HELP_MESSAGE.get('file', ''))

    parser.add_argument('group', help=PARAM_HELP_MESSAGE.get('group', ''), default=[], nargs='*',
                        type=str)
    parser.add_argument('--debug', help='Set logging level to debug',
                        choices=['debug'])

    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.getLevelName(args.debug.upper()))
        logger.debug('Debug mode: ON')

    logger.debug(args)

    file = getattr(args, 'file', None)
    if not file and sys.stdin.isatty():
        parser.print_help()
        exit(2)
    try:
        input_data = json.load(open(file))
    except (ValueError, json.JSONDecodeError, TypeError) as e:
        logger.debug(f'INPUT: {"".join(input_data)}')
        logger.debug(e)
        sys.stderr.write(f'Could not parse JSON\n')
    else:
        try:
            nest = JsonParser(input_data, args.group)
            nested = nest.parse()
        except Exception as e:
            logger.error(e)
            sys.stderr.write(f'Could not create nested dictionary\n')
        else:
            logger.debug(f'OUTPUT LENGTH: {len(nested)}')
            sys.stdout.write(f'{nested}\n')
