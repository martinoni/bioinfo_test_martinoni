#!/usr/bin/env python
# coding: utf-8

# In[5]:


from flask import Flask, escape, request
from postgres_to_json import return_json
from crawler_postgres import crawler


# In[2]:


app = Flask(__name__)


# In[3]:


@app.route('/username=<username>&password=<password>&db=<db>/run/<lista>')
def run(lista, username='', password='', db=''):
    lista = str(lista).replace('[', '').replace(']', '').replace(' ', '').split(',')
    jason = return_json(lista, username, password, db)
    return jason

@app.route('/username=<username>&password=<password>&db=<db>/update')
def baixa(username='', password='', db=''):
    crawler(username, password, db)
    return 'Base de dados pronta!'

