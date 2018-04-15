# OntEnrich
Application for ontology enrichment through linking with DBpedia.

## Setup
```bash
pip install requirements.txt
```
or
```cmd
python -m pip install requirements.txt
```

If you fail to install all libraries at once, then execute `pip install` manually for every library in the `requirements.txt`.

## Usage
For enriching the ontology, first specify all the properties in the `options.json` file:

| Name | Description | Example |
| ---- | ----------- | ------- |
| input_file | Path to the ontology in .ttl fromat | `"ttl/sto.ttl"` |
| whitelist | List of predicates to fetch from DBpedia while enriching | `[ "<http://purl.org/dc/terms/subject>" ]` |
| blacklist | List of predicates to exclude from enrichment process | `[ "http://purl.org/voc/vrank#hasRank" ]` |
| prefixes | List of prefixes to assign to the resulting ontology | `[ { "prfx": "deo", "uri": "http://purl.org/spar/deo/" } ]` |

Next, navigate to the `src` folder and execute `enrich.py` with `options.json` as a parameter:
```bash
python enrich.py --options options.json
```

You are able to execute class cleaning (useful for enriched ontology from the dbpedia):
```bash
python class_cleaning.py --ontology ttl/sto(enriched).ttl
```

In addition, it is possible to check the ontology against the template specified as `template.json` in the `src` folder:
```bash
python template.py --ontology ttl/sto.ttl
```
The logs can be found in the `template_logs.txt` file.

## Example
Using a Turtle format of the [Standard Ontology (STO)](https://github.com/i40-Tools/StandardOntology) as an input for the app, without specifying `whitelist` and `blacklist` in the `options.json` (fetching everything), the following results can be achieved:

| # of linked subjects | # of added triples |
| -------------------- | ------------------ |
| 78 | 8268 |

## License
MIT License. Copyright (c) 2018 Maxim Maltsev.
