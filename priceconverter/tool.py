"""CLI entry point."""
from argparse import ArgumentParser
import sys
from typing import Type

from priceconverter import config, util
from priceconverter.apis import Rates, UnsupportedCurrency


def main() -> None:
    """CLI entry point."""
    parser = ArgumentParser()
    parser.add_argument('price',
                        help='Price to convert',
                        type=util.parse_price)
    parser.add_argument('to',
                        help='Currency to convert to',
                        nargs='?',
                        type=util.parse_currency,
                        default=config.BASE)
    parser.add_argument('--base',
                        help='Conert using a different base currency',
                        nargs='?',
                        type=util.parse_currency,
                        default=None)
    parser.add_argument('--rates-sources',
                        help='Rates sources to use',
                        nargs='+',
                        type=util.parse_rates_sources,
                        default=config.RATES_SOURCES)
    parser.add_argument('--cache-age',
                        help='Max cache age',
                        nargs='?',
                        type=util.parse_timedelta,
                        default=config.CACHE_AGE)
    parser.add_argument('--cache-location',
                        help='Cache location',
                        nargs='?',
                        default=config.CACHE_LOCATION)
    parser.add_argument('--verbose', '-v',
                        help='Verbose output',
                        action='store_true')
    args = parser.parse_args()

    # Debug config
    if args.verbose:
        print(f'Config:\n'
              f'  BASE={config.BASE!r}\n'
              f'  RATES_SOURCES={config.RATES_SOURCES!r}\n'
              f'  CACHE_AGE={config.CACHE_AGE!r}\n'
              f'  CACHE_LOCATION={config.CACHE_LOCATION!r}',
              file=sys.stderr)
        print(f'Args:\n'
              f'  price={args.price!r}\n'
              f'  to={args.to!r}\n'
              f'  base={args.base!r}\n'
              f'  rates_sources={args.rates_sources!r}\n'
              f'  cache_age={args.cache_age!r}\n'
              f'  cache_location={args.cache_location!r}',
              file=sys.stderr)
        print('Calc:', file=sys.stderr)

    # Try and convert
    currency, amount = args.price
    for rates_source_cls in args.rates_sources:
        rates_source_cls: Type[Rates]
        rates_source = rates_source_cls(args.cache_age,
                                        args.cache_location,
                                        args.base or args.to)
        try:
            rate = rates_source.get(currency, args.to)
        except UnsupportedCurrency as e:
            if args.verbose:
                print(f'  {rates_source}: missing {e} rate', file=sys.stderr)
        else:
            if args.verbose:
                print(f'  {rates_source}: {amount} * {rate}', file=sys.stderr)
            print(amount * rate)
            sys.exit(0)
    print(f'No rates source supports {currency} to {args.to}', file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    main()
