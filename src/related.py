from landscape import Ontology, DBpedia


def main():
    ont = Ontology('ttl/sto(enriched).ttl')
    ont_query = """
        PREFIX sto: <https://w3id.org/i40/sto#>
        SELECT ?sub ?obj WHERE {
            ?sub sto:relatedTo ?obj .
        }
    """
    related = {}
    for row in ont.query(ont_query):
        sub = str(row[0])
        obj = str(row[1])
        if sub not in related:
          related[sub] = []
        related[sub].append(obj)
    
    related_simm = related.copy()
    cnt = 0
    for sub in related:
        for obj in related[sub]:
            if obj in related_simm:
                if sub not in related_simm[obj]:
                    related_simm[obj].append(sub)
                    cnt += 1
            else:
                related_simm[obj] = [sub]

    related_tran = related.copy()
    ind = 0
    for sub in related_tran:
        deep(sub, related_tran, related_tran[sub])
    
    print(cnt, ind)

    for sub in related_tran:
        for obj in related_tran[sub]:
            sub = { 'value': sub }
            pred = { 'value': 'https://w3id.org/i40/sto#relatedTo' }
            obj = { 'value': obj }
            ont.enrich(sub, pred, obj)
    
    print('Property sto:relatedTo added to ' + str(len(related_tran) - len(related)) + ' standards')
    ont.export('ttl/sto(full).ttl')


def deep(sub, related_tran, st_related_tran):
    for st in st_related_tran:
        if st != sub:
            if st not in related_tran[sub]:
                related_tran[sub].append(st)
            related_tran = deep(st, related_tran, related_tran[st])
    return related_tran

if __name__ == '__main__':
    main()
