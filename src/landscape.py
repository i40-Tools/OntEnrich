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
        self.graph.add((sub, pred, obj))


    def remove(self, sub=None, pred=None, obj=None):
        """Removes triple from ontology.
        """
        self.graph.remove((URIRef(sub), URIRef(pred), URIRef(obj)))
        

    def check_triple(self, triple):
        """Returns True if triple is in ontology and False o/w.
        """
        # If URI, check links both starting from http and https and remove http
        tmp_triple = triple.copy()
        if str(tmp_triple[2]).find('http') > -1:
            obj = str(tmp_triple[2])
            obj = obj.replace('https:', 'http:')
            tmp_triple[2] = URIRef(obj)
            if tmp_triple in self.graph:
                self.graph.remove(tmp_triple)
                return False
            obj = obj.replace('http:', 'https:')
            tmp_triple[2] = URIRef(obj)
        if tmp_triple in self.graph:
            return True
        return False

    def check_standard(self, standard_name):
        """Returns True if standard is in ontology and False o/w.
        """
        sub = URIRef('https://w3id.org/i40/sto#' + standard_name)
        pred = RDF.type
        obj = URIRef('https://w3id.org/i40/sto#Standard')
        return self.check_triple((sub, pred, obj))

    def check_types(self, obj, types):
        """Checks type of the object.
        """
        for obj_type in types:
            if obj_type == 'Literal' and type(obj) is Literal or \
               obj_type == 'URIRef' and type(obj) is URIRef:
                return True
        return False

    def set_prefix(self, prefix, url):
        """Sets ontology prefixes.
        """
        self.graph.bind(prefix, url)

    def query(self, query):
        """Qyeries data from the ontology.
        """
        return self.graph.query(query)

    def enrich(self, sub, pred, obj):
        """Enriches the ontology based on existing subject and its triples from other source.
        Returns information regarding the number of enriched entities.
        """
        pred_val = URIRef(pred['value'])
        sub_val = URIRef(sub['value'])
        obj_val = obj['value']
        obj_type = obj.get('type') or 'uri'

        if obj_type == 'uri':
            triple = [sub_val, pred_val, URIRef(obj_val)]
        elif obj_type == 'literal' or obj_type == 'typed-literal':
            obj_lang = obj.get('xml:lang')
            obj_datatype = obj.get('datatype')
            triple = [sub_val, pred_val, Literal(obj_val, obj_lang, datatype=obj_datatype)]
        elif obj_type == 'bnode':
            triple = [sub_val, pred_val, BNode(obj_val)]
        else:
            print('!! Error while enriching: wrong obj_type ' + obj_type + ' for ' + sub)
            return False
        if not self.check_triple(triple):
            self.graph.add(triple)
            return True
        return False
