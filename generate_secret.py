#!/usr/bin/env python3
"""Generate a secure SECRET_KEY for JWT signing.

Outputs:
- urlsafe: a URL-safe base64 string (good for env vars)
- hex: a hex string (good for storage or copying)
Use one of these values as your SECRET_KEY.
"""

import secrets
import argparse


def generate_urlsafe(n_bytes: int = 32) -> str:
    return secrets.token_urlsafe(n_bytes)


def generate_hex(n_bytes: int = 32) -> str:
    return secrets.token_hex(n_bytes)


def main():
    parser = argparse.ArgumentParser(description='Generate a secure SECRET_KEY')
    parser.add_argument('--bytes', '-b', type=int, default=32,
                        help='Number of random bytes (default: 32 -> 256 bits)')
    parser.add_argument('--format', '-f', choices=['urlsafe', 'hex', 'both'], default='both',
                        help='Which format to print (default: both)')
    args = parser.parse_args()

    if args.format in ('urlsafe', 'both'):
        print('URL-safe token (good for env vars):')
        print(generate_urlsafe(args.bytes))
    if args.format in ('hex', 'both'):
        print('\nHex token:')
        print(generate_hex(args.bytes))


if __name__ == '__main__':
    main()
