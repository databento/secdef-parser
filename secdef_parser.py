#!/usr/bin/env python3
"""secdef_parser.py: Tool to parse secdef and find most active instruments"""

import os
import sys
import urllib.request as request
import gzip
from argparse import ArgumentParser
from contextlib import closing
from io import BytesIO

import pandas as pd


VERSION = '0.1.0'

SECDEF_URL = "ftp://ftp.cmegroup.com/SBEFix/Production/secdef.dat.gz"

SECDEF_MAP = {'207': 'SecurityExchange',
              '1151': 'SecurityGroup',
              '55': 'Symbol',
              '167': 'SecurityType',
              '462': 'UnderlyingProduct',
              '5792': 'OpenInterestQty'}

ASSET_CLASS_MAP = {'2': 'Commodity/Agriculture',
                   '4': 'Currency',
                   '5': 'Equity',
                   '12': 'Other',
                   '14': 'Interest Rate',
                   '15': 'FX Cash',
                   '16': 'Energy',
                   '17': 'Metals'}

DEFAULT_INPUT = 'secdef.dat.gz'
DEFAULT_OUTPUT = 'list.csv'

secdef_keys = SECDEF_MAP.keys()


def download_secdef():
    """
    Downloads secdef file from CME FTP server into in-memory object
    """
    print("Downloading secdef file...")

    try:
        with closing(request.urlopen(SECDEF_URL)) as response:
            content_raw = response.read()
    except Exception as e:
        print(e.message)
        print("Unable to access secdef from CME FTP server")
        sys.exit(1)

    print("Download complete, decompressing...")

    content = gzip.GzipFile(fileobj=BytesIO(content_raw)).read()
    return content.decode('utf8')


def process_row(row):
    """
    Extracts only the fields we are interested in and converts them to
    key-value representation
    """
    return dict((k, v) for k, v in zip(row[::2], row[1::2])
                if k in secdef_keys)


def parse_secdef(secdef_raw):
    """
    Parses raw, uncompressed secdef data and generates cleaned dataframe
    with aggregate open interest quantity
    """

    print("Parsing secdef data... this could take a minute...")

    # Split by row and remove empty rows
    secdef_raw = [l for l in secdef_raw.split('\n') if l]

    # Parse FIX format and prepare key-value representation for dataframe
    secdef_csv = ['='.join(x.rstrip('\x01').split('\x01')).split('=') for x in
                  secdef_raw]
    data = map(process_row, secdef_csv)

    # Generate dataframe
    df = pd.DataFrame(data)

    # Convert fields to friendly names
    df.rename(columns=SECDEF_MAP, inplace=True)

    # Rearrange columns
    df = df[['SecurityExchange',
             'SecurityGroup',
             'Symbol',
             'SecurityType',
             'UnderlyingProduct',
             'OpenInterestQty']]

    # Remove nulls
    df.dropna(inplace=True)

    # Convert str quantities to integer type
    df['OpenInterestQty'] = df['OpenInterestQty'].astype(int)

    # Remove non-futures instruments
    df = df[df['SecurityType'] == 'FUT']

    # Aggregate open interest by security group
    agg = df.groupby(['SecurityExchange', 'SecurityGroup',
                     'UnderlyingProduct'], as_index=False).sum()

    return agg


def main():

    # Current path
    this_file_dir = os.path.dirname(os.path.realpath(__file__))

    # Parse arguments
    parser = ArgumentParser(description="Tool to parse secdef and find most \
                            active instruments")

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-i',
                       type=str,
                       default=DEFAULT_INPUT,
                       metavar='SECDEF_FILE',
                       help="Input secdef.dat or secdef.dat.gz file \
                            (default=secdef.dat.gz)",
                       dest='input')
    group.add_argument('-d',
                       '--download',
                       action='store_true',
                       default=False,
                       help="Download data from CME FTP server (default=off)",
                       dest='download')

    parser.add_argument('-o',
                        type=str,
                        default=os.path.join(this_file_dir, DEFAULT_OUTPUT),
                        help="Output CSV file listing most active instruments \
                            (default=list.csv)",
                        dest='output')

    parser.add_argument('--version',
                        action='store_true',
                        default=False,
                        help="Prints version number",
                        dest='version')

    args = parser.parse_args()

    if args.version:
        print(VERSION)
        sys.exit(0)

    if args.download:
        secdef_raw = download_secdef()

    else:
        # Error-checking: -i
        if not os.path.isfile(args.input):
            print("Unable to find specified input secdef file")
            sys.exit(1)

        bname, ext = os.path.splitext(os.path.basename(args.input))

        if ext == '.gz':
            # Expect compressed secdef file
            with gzip.open(args.input, 'rb') as f:
                secdef_raw = f.read().decode('utf8')

        else:
            # Expect uncompressed secdef file
            with open(args.input, 'r') as f:
                secdef_raw = f.read()

    try:
        agg = parse_secdef(secdef_raw)
    except Exception as e:
        print(e.message)
        print("Failed to parse secdef file, check if your file is corrupted")
        sys.exit(1)

    # Make output pretty
    agg['UnderlyingProduct'] = agg['UnderlyingProduct']\
        .apply(lambda k: ASSET_CLASS_MAP.get(k))
    agg.sort_values(by='OpenInterestQty', ascending=False, inplace=True)

    try:
        agg.to_csv(args.output, index=False)
    except Exception as e:
        print(e.message)
        print("Failed to write output file, check if directory exists")
        sys.exit(1)


if __name__ == '__main__':
    main()
