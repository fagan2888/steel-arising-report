"""Sankey Diagram Definition for the UK model.

Created by Rick Lupton, 13 March 2019.

"""

from floweaver import *

sectors = ['4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15a', '15b', '16', '17', '18', '19', '20']

sector_labels = [
 'Bolts, nuts, rivets, screws, etc.',
 'Hand tools, cutlery, instrument engineering',
 'Packaging and industrial and domestic hollow-ware',
 'Other metal goods (including furnitue, doors, windows, non-electric domestic appliances, and springs)',
 'Electrical engineering, including elec. domestic appliances',
 'Agricultural machinery',
 'Metal working toolsand engineering tools',
 'Construction, earth moving and mechanical handling equipment',
 'Other mechanical engineering',
 'Industrial and process plant',
 'Construction and fabricated constructional steelwork',
 'Motor vehicles: BIW',
 'Motor vehicles: drivetrain, chassis, and trimmings',
 'Other transport',
 'Coal, coke, petroleum and natural gas',
 'Gas, electricity and water',
 'Chemical and allied industries',
 'Other UK consumers']

products = ['Hot rolled', 'Plate', 'Cold rolled', 'Hot dipped galvanised',
            'Electro coated', 'Organic coated', 'Tin plate', 'Tubes and pipes',
            'Railway track material', 'Sheet piling and rolled accessories',
            'Heavy sections', 'Light sections',
            'Hot rolled bars in lengths', 'Bright bars', 'Reinforcing bar', 'Rods']

##### PARTITIONS #####
# These define the level of detail and labels for the products and sectors

# This is the level of detail for the semi-finished steel products waypoint
p_products = Partition.Simple('material', products)

# This is the level of detail for demand sectors
p_sectors = Partition.Simple('material', [
    (name, [code]) for code, name in zip(sectors, sector_labels)
])

# This is the level of detail for manufacturing -- more complicated because
# the "sector X" and "products X" are separate nodes in the flow data.
manufac_and_products = [
    (sector, ['sector %s' % sector, 'products %s' % sector])
    for sector in sectors
]
p_manufac = Partition.Simple('process', manufac_and_products)

# This is the level of detail for the colours
p_materials = Partition.Simple('material', [
    ('Flat', ['Hot rolled', 'Plate', 'Cold rolled', 'Hot dipped galvanised',
              'Electro coated', 'Organic coated', 'Tin plate', 'Tubes and pipes']),
    ('Long', ['Railway track material', 'Sheet piling and rolled accessories', 'Heavy sections', 'Light sections',
              'Hot rolled bars in lengths', 'Bright bars', 'Reinforcing bar', 'Rods']),
    ('Metal goods', ['4', '5', '6', '7']),
    ('Elec. eng', ['8']),
    ('Mech. eng', ['9', '10', '11', '12', '13']),
    ('Construction', ['14']),
    ('Transport', ['15a', '15b', '16']),
    ('Energy/water', ['17', '18', '19']),
    ('Other', ['20']),
    'component',
    ('scrap', ['scrap %s' % p for p in products])
])

##### STRUCTURE #####
# These are the groups and waypoints defining the structure of the Sankey diagram
nodes = {
    # Main nodes: production to manufacturing to demand
    'prod': ProcessGroup(['uk_production'], title='UK production'),
    'semi': Waypoint(p_products, title='Steel products'),
    'manuf': ProcessGroup([yy for xx in manufac_and_products for yy in xx[1]],
                          p_manufac, title='Manufacturing'),
    'demand': ProcessGroup(['uk_demand'], p_sectors, title='UK demand'),

    # Scrap output from manufacturing
    'scrap': ProcessGroup(['scrap'], title='Manufacturing scrap'),

    # Imports and exports
    'semi_export': ProcessGroup(['exports'], title='Export of steel products'),
    'semi_import': ProcessGroup(['imports'], title='Import'),
    'comp_import': ProcessGroup(['component_imports'], title='Import components'),
    'prod_export': ProcessGroup(['product_exports'], title='Export of goods'),
    'prod_import': ProcessGroup(['product_imports'], title='Import of steel-containing goods'),

    'imbalance': ProcessGroup(['imbalance'])
}

ordering = [
    [['semi_import'], ['prod'], []],
    [['comp_import', 'imbalance'], ['semi'], ['semi_export']],
    [['prod_import'], ['manuf']],
    [[], ['demand'], ['prod_export', 'scrap']],
]

bundles = [
    # Main flow: production to manufacturing to demand
    Bundle('prod', 'manuf', waypoints=['semi']),
    Bundle('manuf', 'demand'),

    # Scrap output from manufacturing
    Bundle('manuf', 'scrap'),

    # Imports and exports
    Bundle('prod', 'semi_export'),
    Bundle('manuf', 'prod_export'),

    Bundle('semi_import', 'manuf', waypoints=['semi']),
    Bundle('comp_import', 'manuf'),
    Bundle('prod_import', 'demand'),

    Bundle('imbalance', 'manuf'),
]

sdd = SankeyDefinition(nodes, bundles, ordering, flow_partition=p_materials)

# Define the colours:
from palettable.cartocolors.qualitative import Prism_10, Antique_10
C = Prism_10.hex_colors[1:]

palette = {k: '#999' for k in p_materials.labels}
palette['Flat'] = Antique_10.hex_colors[0]
palette['Long'] = Antique_10.hex_colors[2]
palette['Metal goods'] = C[0]
palette['Elec. eng'] = '#499dd9'
palette['Mech. eng'] = C[2]
palette['Construction'] = '#8cc425'
palette['Transport'] = C[4]
palette['Energy/water'] = '#cc4520'
palette['Other'] = '#8f1e76'
palette['component'] = Antique_10.hex_colors[1]
