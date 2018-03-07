"""Module that describes all commonly used methods for enriching ontologies.
"""

from rdflib import Graph, Literal, BNode, URIRef
from rdflib.namespace import RDF
from SPARQLWrapper import SPARQLWrapper, JSON

class DBpedia:
    """Describes all possible approaches to extract data from DBpedia.
    """

    def query(self, query):
        """Queries data from dbpedia.
        """
        sparql = SPARQLWrapper('http://dbpedia.org/sparql')
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return results['results']['bindings']

class Blacklist(list):
    """Describes which predicates should be excluded while enriching the ontology.
    """

    def add(self, pred):
        """Adds a predicate to the blacklist.
        """
        self.append(pred)

    def remove(self, pred):
        """Removes a predicate from the blacklist.
        """
        self.remove(pred)

    def check(self, pred):
        """Checks whether the predicate is in the black list.
        """
        if pred in self:
            return True
        else:
            return False

class Ontology(object):
    """A semantic ontology. Ontologies have the following properties:

    Attributes:
        path: A string representing the path to ontology.
        name: A string representing the name of ontology.
        blacklist: A list of the predicates to exclude while enriching.
    """

    def __init__(self, path, name='Ontology'):
        """Initializes a semantic ontology.
        """
        self.name = name
        self.graph = Graph().parse(path, format='turtle')
        self.blacklist = Blacklist()

    def export(self, filename):
        """Saves generated ontology as a turtle file.
        """
        self.graph.serialize(destination=filename, format='turtle')

    def add(self, sub, pred, obj):
        """Adds triple to ontology.
        """
        self.graph.add([sub, pred, obj])

    def remove(self, sub=None, pred=None, obj=None):
        """Removes triple from ontology.
        """
        self.graph.remove([sub, pred, obj])

    def check(self, sub, pred=None, obj=None):
        """Returns True if triple is in ontology and False o/w.
        By default (with pred and obj not specified) checks if it is an sto:Standard.
        """
        sub = URIRef('https://w3id.org/i40/sto#' + sub)
        if not pred and not obj:
            pred = RDF.type
            obj = URIRef('https://w3id.org/i40/sto#Standard')
        if (sub, pred, obj) in self.graph:
            return True
        else:
            return False

    def set_prefix(self, prefix, url):
        """Sets ontology prefixes.
        """
        self.graph.bind(prefix, url)

    def query(self, query):
        """Qyeries data from the ontology.
        """
        return self.graph.query(query)

    def enrich(self, sub, source):
        """Enriches the ontology based on existing subject and its triples from other source.
        """
        for triple in source:
            pred = triple['pred']['value']
            if pred not in self.blacklist:
                if sub is None:
                    sub = URIRef(triple['sub']['value'])
                pred = URIRef(pred)
                obj = triple['obj']
                obj_val = obj['value']
                obj_type = obj['type']
                lang = 'xml:lang'

                if obj_type == 'uri':
                    self.graph.add([sub, pred, URIRef(obj_val)])
                elif obj_type == 'literal':
                    if lang in obj:
                        obj_lang = obj['xml:lang']
                        self.graph.add([sub, pred, Literal(obj_val, obj_lang)])
                    else:
                        self.graph.add([sub, pred, Literal(obj_val)])
                elif obj_type == 'typed-literal':
                    obj_datatype = obj['datatype']
                    if lang in obj:
                        obj_lang = obj['xml:lang']
                        self.graph.add([sub, pred, \
                            Literal(obj_val, obj_lang, datatype=obj_datatype)])
                    else:
                        self.graph.add([sub, pred, Literal(obj_val, datatype=obj_datatype)])
                elif obj_type == 'bnode':
                    self.graph.add([sub, pred, BNode(obj_val)])
                else:
                    print('---UNKNOWN OBJECT TYPE ' + obj_type + ' FOR ' + sub + '---')
