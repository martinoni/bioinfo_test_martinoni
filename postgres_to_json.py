#!/usr/bin/env python
# coding: utf-8

# In[31]:


import pandas as pd
import requests
from bs4 import BeautifulSoup 
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO
import psycopg2
from sqlalchemy import create_engine
import io
import json
from flask import jsonify


# In[85]:


def return_json(genes_input, username, password, db):
    con = psycopg2.connect(host='localhost', database=db,
                           user=username, password=password)
    cur = con.cursor()
    dados = []
    lista = []
    for gene_input in genes_input:
        sql = 'SELECT * FROM phenotype_to_genes WHERE ' + '"Gene-Name" ' + " = " + gene_input
        cur.execute(sql)
        recset = cur.fetchall()
        dados = recset
        df = pd.DataFrame(dados)
        fenotipos = []
        for tup in df.values:
            d1 = {'hpo': tup[0], 'name': tup[1]}
            fenotipos.append(d1)
        d = {'phenotype': fenotipos, 'gene': tup[3], 'gene_id': tup[2]}
        lista.append(d)
    con.close()
    print(len(lista))
    lista_js = jsonify(lista)
    return lista_js

