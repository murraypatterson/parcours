# parcours

PARsimonious CO-occURrenceS

Infer all possible assignments of ancestral states for a set of
characters in a phylogenetic tree, given extant states and a cost
matrix using Sankoff's algorithm, and then compute the correlation, as
determined by their (co-) occurrence patterns among their respective
ancestral assignments.

# how to run

First, make sure that you have Python3 and NumPy as well as the [ETE
Toolkit](http://etetoolkit.org/).  The latter two can be installed on
most systems with via

    pip3 install numpy
    pip3 install ete3

respectively, if you have `pip`, or through Conda.  Once these
prerequisites are met, simply run the `parcours` executable to run the
tool.  For the full set of parameters of `parcours`, type

    ./parcours -h

# quick example

The easiest way to run `parcours` is through a config file.  Go to the
`example/` directory and type

    ../parcours -f config.csv

to generate the solution for a given instance: a phylogeny `tree.nh`,
a set of extant states `extant.csv` of some characters, and a cost
matrix `cost.csv`.  An ancestral reconstruction appears in
`output.csv`, while all possible ancestral reconstructions for each
character (of `extant.csv`) appears in `solutions/`.  Finally, all
events that happen in the tree for single characters appear in
`unit.csv`, while all events that happen for pairs of characters,
along with their correlation, appear in `pairwise.csv`.  For the full
set of parameters of `parcours`, type

    ../parcours -h

or with no parameters.
