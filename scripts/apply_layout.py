#!/usr/bin/env python

"""Apply layout information to a Sankey JSON file.

Usage:
  apply_layout.py --layout LAYOUT-FILE IN-FILE OUT-FILE

Options:
  --layout LAYOUT-FILE    Filename of the Sankey layout JSON file
"""

import os.path
import json
from docopt import docopt
from logzero import logger

margin_left = 150
margin_top = 50


def node_positions_dict(layout):
    return {
        node['id']: {'x': node['geometry']['x'] + margin_left,
                     'y': node['geometry']['y'] + margin_top,
                     'hidden': node['style']['hidden'],
                     'title': node['title']}
        for node in layout['nodes']
    }


def apply_layout(layout, value):
    """Copy layout from `layout` to `value`."""
    node_positions = node_positions_dict(layout)
    for node in value['nodes']:
        if node['id'] in node_positions:
            node.update(node_positions[node['id']])
        else:
            logger.warning('No node position for "%s"', node['id'])

    # Copy the page size and scale from the layout Sankey:
    value['pageSize'] = layout['dimensions']
    value['scale'] = layout['metadata']['scale']
    return value



def main(layout_filename, input_filename, output_filename):
    print(layout_filename, input_filename, output_filename)
    # Load the layout file, and build a map of node positions:
    with open(layout_filename, 'r') as f:
        layout = json.load(f)

    # Load the Sankey data and apply layout
    with open(input_filename, 'r') as f:
        data = json.load(f)

    data = apply_layout(layout, data)

    with open(output_filename, 'wt') as f:
        json.dump(data, f)


if __name__ == '__main__':
    args = docopt(__doc__)
    main(args['--layout'], args['IN-FILE'], args['OUT-FILE'])
