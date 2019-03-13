import pandas as pd
import datapackage


def load_dataframe(filename, resource):
    """Load one table from a datapackage."""
    package = datapackage.Package(filename)
    r = package.get_resource(resource)
    return pd.DataFrame(r.read(), columns=r.headers)


def load_datapackage_tables(filename):
    """Load all the tables from a datapackage."""
    package = datapackage.Package(filename)
    tables = {
        r.name: pd.DataFrame(r.read(), columns=r.headers)
        for r in package.resources
    }
    return {
        k: df.set_index(['year', 'product'])
        for k, df in tables.items()
    }


# from https://stackoverflow.com/a/49601444/1615465
def lighten_color(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])
