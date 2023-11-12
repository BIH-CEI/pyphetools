# Validation


There are many types of errors that can occur in phenopackets. The Java application [phenopacket-tools](https://github.com/phenopackets/phenopacket-tools) is a general purpose app for validating and working with phenopackets. pyphetools provides a limited number of commands to check validity of the generated phenoopackets that can be conveniently used as a part of notebooks that create phenopackets.

Commonly encvountered errors include redundancy and inheritance conflicts.

### Mistaken HPO identifiers or labels

Sometimes a phenopacket may contain an obsolete HPO id or a spelling error in the label.

### Redundant terms

If an individual is found to have [Nuclear cataract(HP:0100018)](https://hpo.jax.org/app/browse/term/HP:0100018){:target="\_blank"}, which means an opacity that develops in the nucleus of the lens of the eye, then the individual always can be said to have a   [Cataract (HP:0000518)](https://hpo.jax.org/app/browse/term/HP:0000518){:target="\_blank"}, which refers to an opacity anywhere in the lens of the eye. This is because of the so-called true-path rule of ontologies, according to which if an HPO term is used to annotate an individual, then the parent of that term and all of the ancestors of that term must also apply. In this case, Cataract is a grand-parent of Nuclear cataract.

Because of this, if we have annotated with [Nuclear cataract(HP:0100018)](https://hpo.jax.org/app/browse/term/HP:0100018){:target="\_blank"}, it is not necessary to annotate with [Cataract (HP:0000518)](https://hpo.jax.org/app/browse/term/HP:0000518){:target="\_blank"}, because it is implicitly true.

We therefore recommend that only the most specific HPO term be used for a time point.

### Conflicting terms

In some datasets we have seen, a patient is annotated with a specific term in an organ, but also indicate that abnormalities have been excluded at a higher level. For instance, we might see [Ventricular septal hypertrophy (HP:0005144)](https://hpo.jax.org/app/browse/term/HP:0005144) but also excluded [Abnormal heart morphology (HP:0001627)](https://hpo.jax.org/app/browse/term/HP:0001627).


## QC with pyphetools.
We recommned checking all generated phenopackets with the following steps.

### Input

After creating phenopackets with pyphetools, we will have access to a collection of phenopacket objects in the Jupyter notebook environment. They can be generated as follows.

```python title="Generating GA4GH phenopackets from a pyphetools individual list"
ppacket_list = [i.to_ga4gh_phenopacket(metadata=metadata.to_ga4gh()) for i in individuals]
```

Alternatively, to ingest a set of phenopackets from files, use the code shown in the documentation
for the [content validator](../api/validation/content_validator.md).

### ContentValidator

Create a [ContentValidator](../api/validation/content_validator.md) for the phenopackets. This object
checks that the generated phenopackets have a minimum number of HPO terms, alleles, and variants.

```python title="Generating GA4GH phenopackets from a pyphetools individual list"
validator = ContentValidator(min_var=1, min_hpo=3)
errors = validator.validate_phenopacket_list(ppkt_list)
```