#!/usr/bin/env python

"""Generate Sankey JSON data for each year.

Usage:
  generate_sankey_data.py FLOWS-DATAPACKAGE YEAR OUTPUT-FILE

"""

import json
from docopt import docopt
import pandas as pd
from floweaver import weave

from util import load_dataframe
from sankey_definition import sdd, palette


def main(flows_datapackage, year, output_file):
    flows = load_dataframe(flows_datapackage, 'flows')
    data = weave(sdd, flows.query('year == @year'), palette=palette).to_json()

    data['metadata']['title'] = str(year)

    with open(output_file, 'wt') as f:
        json.dump(data, f)

if __name__ == '__main__':
    args = docopt(__doc__)
    main(args['FLOWS-DATAPACKAGE'], args['YEAR'], args['OUTPUT-FILE'])
