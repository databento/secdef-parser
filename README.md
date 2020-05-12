# secdef-parser

This project contains a command line tool that demonstrates how to parse secdef
files found on [CME's public FTP server](ftp://ftp.cmegroup.com/SBEFix/Production/). 
For the purpose of this demonstration, the tool generates a list of the most
active futures products ranked by open interest.  


# About secdef files

The secdef file contains useful production instrument definition data and 
settlement prices formatted as concatenated FIX (plaintext) messages. You can 
learn more about the message specifications [here](https://www.cmegroup.com/confluence/display/EPICSANDBOX/MDP+3.0+-+Security+Definition)
especially if you want to parse other fields from the secdef files besides the ones 
extracted by this tool.

CME updates its secdef files almost daily. However, for intraday instrument 
definition updates, you should not be using this approach.

More information about secdef files can be found [here](ftp://ftp.cmegroup.com/SBEFix/Production/secdef_disclaimer.txt).


# Requirements

Required:
- Python >= 3.4
- pandas >= 0.24.2

Recommended:
- Minimum 4 GB free memory. secdef files often contain 400k+ instrument 
definitions which comes to 300+ MB uncompressed. This tool is not optimized 
for low memory devices and uses substantial amount of memory to parse the
secdef files relatively quickly. 


# Installation

Clone this repository.

```
git clone https://github.com/databento/secdef-parser.git
cd secdef-parser
```

# Usage

By default, the parser will look for `secdef.dat.gz` as the input secdef file 
in your local directory and write the output as comma-separated 
values to `list.csv`.

First, [download a copy of the secdef file](ftp://ftp.cmegroup.com/SBEFix/Production/secdef.dat.gz)
from CME. Then run the parser:

```bash
# Run with default input and output
$ python secdef_parser.py
```

You can change the parameters:

```bash
# Parse a regular (compressed) secdef file
$ python secdef_parser.py -i secdef.dat.gz

# Alternatively, parse a decompressed secdef file
$ python secdef_parser.py -i secdef.dat

# Write to a specific location
$ python secdef_parser.py -o path/to/my/output.csv
```

For your convenience, the command line tool can download the secdef file
directly for you.
```bash
$ python secdef_parser.py --download -o path/to/my/output.csv
```


# Results

Here are the top 40 most active products on May 11, 2020.

```
SecurityExchange,SecurityGroup,UnderlyingProduct,OpenInterestQty
XCME,GE,Interest Rate,10743955
XCBT,ZF,Interest Rate,3618711
XCBT,ZN,Interest Rate,3391115
XCME,ES,Equity,3265839
XNYM,CL,Energy,3003110
XCBT,ZT,Interest Rate,2447405
XNYM,NG,Energy,2217482
XCBT,ZS,Commodity/Agriculture,1729122
XCBT,ZQ,Interest Rate,1719442
XCBT,ZC,Commodity/Agriculture,1395498
XNYM,PW,Energy,1131339
XCBT,ZU,Interest Rate,1061430
XCBT,ZB,Interest Rate,1002804
XCBT,Z1,Interest Rate,888267
XNYM,CC,Energy,761722
XCME,6E,Currency,562127
XCME,RY,Equity,531217
XCEC,GC,Metals,526345
XCME,SS,Interest Rate,430569
XCBT,ZW,Commodity/Agriculture,346276
XNYM,HX,Energy,282184
XCME,LE,Commodity/Agriculture,267117
XCME,NQ,Equity,243555
XNYM,OP,Energy,232991
XNYM,ZZ,Other,226829
XCME,0B,Equity,226530
XKLS,BC,Commodity/Agriculture,216524
XCBT,KE,Commodity/Agriculture,212212
XCME,HE,Commodity/Agriculture,200599
XNYM,PT,Energy,193133
XCEC,HG,Metals,177534
XCME,6B,Currency,163511
XCME,6J,Currency,160269
XCME,SD,Equity,146997
XCEC,SI,Metals,141423
XCME,6A,Currency,138974
XNYM,GS,Energy,130863
XCME,6C,Currency,120412
XCME,MS,Equity,111053
XCME,SP,Equity,103459
```

To understand the SecurityGroup codes, use the [CME Product Slate](https://www.cmegroup.com/trading/products/).
Not surprisingly, Eurodollar futures are by far the most active among 
outrights, followed by US Treasury products, ES and crude oil.


# Historical secdef files

For additional, historical secdef data, you can find a free batch of secdef 
files from Dec 2019 hosted by Databento [here](https://s3.amazonaws.com/databento.com/samples/sample-cme-secdef-201912.zip).
To learn more about Databento, visit us at [https://databento.com/](https://databento.com).


# Release notes

*0.1.0*
- Initial release


# License

This project is licensed and made available under the terms of the MIT 
License. See the contained `LICENSE` file for specific language.
