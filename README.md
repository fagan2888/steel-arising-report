# Figures for the Steel Arising report

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2592572.svg)](https://doi.org/10.5281/zenodo.2592572)

This repository contains scripts and layout files to create the figures in the
Steel Arising report.

**The built figure files are available via [the latest
release](https://github.com/ricklupton/steel-arising-report/releases/latest)**

## Data dependencies

The model uses the data in the
[uk-steel-model](https://github.com/ricklupton/uk-steel-model) repository. This
contains information on production, imports, exports, manufacturing and demand
for steel products and steel-containing goods in the UK, from 1980 to 2016.

## Preparation

The dependencies for this model are installed using `Pipenv` and `npm`.

Make sure required Python packages are installed:

```shell
$ pipenv install
```

Unfortunately this may fail to install the first time due to the use of the
`future_fstrings` package by the script for getting data from Zenodo. To fix it:

```shell
$ pipenv run pip install future_fstrings
$ pipenv install
```

Install `svg-sankey`:

```shell
$ npm install -g svg-sankey   # you might need to add "sudo" to the beginning
```

Build the figures and Sankey diagrams:

```shell
$ make
```

## Sankey diagrams

The Sankey diagram SVG files for each year are output into the
`build/sankey_svgs` folder. Figure 13 in the report was created by adding the
annotations saved in `figures_manual/sankey_annotation.svg`.

## Figures

The rest of the figures are saved as PDFs into the `figures` folder.
