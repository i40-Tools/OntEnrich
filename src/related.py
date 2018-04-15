from landscape import Ontology, DBpedia
import numpy as np


def main():
    ont = Ontology('ttl/sto(enriched).ttl')
    ont_query = """
        PREFIX sto: <https://w3id.org/i40/sto#>
        SELECT ?sub ?obj WHERE {
            ?sub sto:relatedTo ?obj .
        }
    """
    relations = {}
    standards = []
    for row in ont.query(ont_query):
        sub = str(row[0])
        obj = str(row[1])
        if sub not in standards:
            standards.append(sub)
            relations[sub] = []
        if obj not in standards:
            standards.append(obj)
            relations[obj] = []
        relations[sub].append(obj)
    
    # creating adjacency matrix out of query result
    std_num = len(standards)
    mtx_raw = np.zeros((std_num, std_num))
    for ind, std_sub in enumerate(standards):
        for jnd, std_obj in enumerate(standards):
            if std_obj in relations[std_sub]:
                mtx_raw[ind, jnd] = 1
    
    # updating matrix by implementing symmetric operator
    mtx = mtx_raw.astype(bool)
    mtx = np.bitwise_or(mtx, mtx.T)

    # updating matrix with transitive closures
    # Floyd Warshall algorythm is used
    reach = [i[:] for i in mtx]
    for k in range(std_num):
        for i in range(std_num):
            for j in range(std_num):
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])
    
    # removing relations of standards to themselves
    np.fill_diagonal(mtx, False)

<<<<<<< HEAD
    for sub in related_tran:
        for obj in related_tran[sub]:
            sub = { 'value': sub }
            pred = { 'value': 'https://w3id.org/i40/sto#relatedTo' }
            obj = { 'value': obj }
            ont.enrich(sub, pred, obj)
    
    print('Property sto:relatedTo added to ' + str(len(related_tran) - len(related)) + ' standards')
=======
    # enriching ontology with new triples
    for i in range(std_num):
        for j in range(std_num):
            if mtx[i][j]:
                triple = {
                    'sub': {
                        'value': standards[i],
                    },
                    'pred': {
                        'value': 'https://w3id.org/i40/sto#relatedTo',
                    },
                    'obj': {
                        'value': standards[j],
                        'type': 'uri',
                    }
                }
                ont.enrich(None, [triple])
>>>>>>> 7ad1060fd4154c03b223c19b4f245e666664c172
    ont.export('ttl/sto(full).ttl')

    # counting number of updated standards
    mtx_diff = mtx.astype(int) - mtx_raw
    diff_cnt = np.count_nonzero(mtx_diff)
    print('Number of enriched standards: ', diff_cnt)

if __name__ == '__main__':
    main()
