#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


def crawler(username, password, db):
    req = requests.get('http://compbio.charite.de/jenkins/job/hpo.annotations.monthly/lastStableBuild/artifact/annotation/ALL_SOURCES_ALL_FREQUENCIES_phenotype_to_genes.txt')
    content = req.content
    soup = BeautifulSoup(content, 'html.parser')
    dados_sujos = str(soup)
    dados = dados_sujos.replace('	', '|').replace('<tab>', '|').replace('</tab></tab></tab>', '')
    aux_data = StringIO(""+dados+"")
    df = pd.read_csv(aux_data, sep="|")
    engine = create_engine('postgresql+psycopg2://' + username + ':' + password + '@localhost:5432/' + db)
    df.head(0).to_sql('phenotype_to_genes', engine, if_exists='replace',index=False) #truncates the table
    conn = engine.raw_connection()
    cur = conn.cursor()
    output = io.StringIO()
    df.to_csv(output, sep='\t', header=False, index=False)
    output.seek(0)
    contents = output.getvalue()
    cur.copy_from(output, 'phenotype_to_genes', null="") # null values become ''
    conn.commit()

