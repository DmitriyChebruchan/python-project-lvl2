#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description='Generate diff')
parser.add_argument('first_file')
parser.add_argument('second_file')
args = parser.parse_args()
print(args.echo)


def main():
    print(args.echo)


if __name__ == '__main__':
    main()
