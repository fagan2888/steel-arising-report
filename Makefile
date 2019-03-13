UK_STEEL_MODEL_DOI = 10.5281/zenodo.2592184
UK_STEEL_MODEL_FILENAME = uk-steel-model-v1.0.0.zip
UK_STEEL_MODEL_PATH = build/input_data/$(UK_STEEL_MODEL_FILENAME)

# These are the years of data to create Sankey diagrams for
YEARS := $(shell seq 1980 2016)

# Sankey diagram filenames for each year
SANKEY_TARGETS := $(foreach year,$(YEARS),build/sankey_svgs/sankey_$(year).svg)

LAYOUT_FILE := scripts/sankey_layout.json

# Other figures from the Jupyter notebook

FIGURE_FILES := \
figure12_output_and_final_demand.csv \
figure12_output_and_final_demand.pdf \
figure14_forms_of_imported_steel.pdf \
figure16a_uk_demand_total.pdf \
figure16b_uk_demand_excluding_imported_goods.pdf \
figure16c_uk_demand_excluding_imported_steel_any_form.pdf \
figure30a_uk_manufacturing.pdf \
figure30b_uk_manufacturing_excluding_imported_components.pdf \
figure30c_uk_manufacturing_excluding_imported_steel_any_form.pdf \

.phony: svgs figures all clean

all: svgs figures

clean:
	rm -rf build
	rm figures/*

figures: $(FIGURE_FILES)

svgs: $(SANKEY_TARGETS)

# Data dependencies

$(UK_STEEL_MODEL_PATH):
	mkdir -p build/input_data
	cd build/input_data && pipenv run zenodo_get.py $(UK_STEEL_MODEL_DOI)

# Rule for generating Sankey data
# $* is match for %, $@ is target of rule, $^ is prerequisite
build/sankey_data/sankey_%.json: $(UK_STEEL_MODEL_PATH) scripts/sankey_definition.py
	mkdir -p build/sankey_data
	pipenv run scripts/generate_sankey_data.py $(UK_STEEL_MODEL_PATH) $* $@


# Rule for applying layout to Sankey data
build/sankey_data_with_layout/sankey_%.json: build/sankey_data/sankey_%.json $(LAYOUT_FILE)
	mkdir -p build/sankey_data_with_layout
	pipenv run scripts/apply_layout.py --layout $(LAYOUT_FILE) $< $@


# Rule for converting Sankey data to SVG
build/sankey_svgs/sankey_%.svg: build/sankey_data_with_layout/sankey_%.json
	mkdir -p build/sankey_svgs
	svg-sankey \
	    --margins 0,0,0,30 \
	    --font-size 18 \
	    --size 1500,1050 \
	    --scale 0.02 \
	    --position x,y $< \
	    | sed 's/Helvetica, Arial, sans-serif/Myriad Pro,Helvetica, Arial, sans-serif/g' \
	    > $@


# Build the rest of the figures
$(FIGURE_FILES): figures/.the-figures-are-done
	:

figures/.the-figures-are-done: $(UK_STEEL_MODEL_PATH) scripts/Figures.ipynb
	pipenv run jupyter nbconvert --execute --to notebook scripts/Figures.ipynb
	touch $@


# Bundle everything up
figures.zip: svgs figures
	cp figures_manual/figure13_sankey_2016.pdf figures
	rm $@
	zip -r $@ figures build
