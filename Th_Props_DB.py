# -*- coding: utf-8 -*-
"""
Created on Wed May 13 12:08:24 2020

@author: ACascioli
"""

import pathlib as plib
import sqlite3
import numpy as np

def dup_check(species,species_names,species_cas):
    t = [cas for cas in species_cas if species_cas.count(cas) >= 2]
    t1,t2 = np.split(np.array(t),2)
    # t = list(set(t))
    print(t)
    # print('')
    # print(indxes)
    # print('len spec', len(species))
    for i in t1:
        n = species_cas.index(i)
        del species[n]
        del species_names[n]
        del species_cas[n]

    t = [cas for cas in species_cas if species_cas.count(cas) >= 2]

    if len(t) != 0:
        t = list(set(t))
        print(t)
    else:
        print('All duplicates has been removed...')
    return species,species_names,species_cas

path = plib.Path(__file__).parents[0]
db_name = plib.Path(path,'Th_props.db')

conn = sqlite3.connect(db_name)
c = conn.cursor()

# Create tables one for en and one for de

c.execute('''CREATE TABLE IF NOT EXISTS Critical_Properties(
    Species_CAS text,
    Species_names text,
    Formula text,
    Tc float,
    Pc float,
    Gj0 float,
    MW float,
    HHV float
    )''')

c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS idx_Species_CAS
          ON Critical_Properties(Species_CAS)
          ''')


conn.commit()
conn.close()

def run_query(query, parameters=()):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        query_result = cursor.execute(query, parameters)
        conn.commit()
    return query_result


def add_data(species_cas, species_names, species,
                      Tc, Pc, Gj0, MW, HHV):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = 'INSERT INTO Critical_Properties VALUES (?,?,?,?,?,?,?,?)'

    for i in range(len(species_cas)):
        try:
            parameters = (species_cas[i], species_names[i], species[i],
                          Tc[i], Pc[i], Gj0[i], MW[i], HHV[i])
            run_query(query, parameters)
            print('species CAS: ' + species_cas[i] + ' added to db\n')

        except Exception as e:
            pass
            # print(e)
            # print('species CAS: ' + species_cas[i] + '\n')
    conn.commit()
    conn.close()

def delet_data(species_cas):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = 'DELETE FROM Critical_Properties WHERE species_cas = ?'
    parameters = (species_cas,)
    run_query(query, parameters)

def get_values(species_cas):
    species_names = []
    species = []
    Tc = []
    Pc = []
    Gj0 = []
    MW = []
    HHV = []
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = 'SELECT * FROM Critical_Properties WHERE Species_CAS = ?'
    for cas in species_cas:
        parameters = (cas,)
        res = run_query(query, parameters).fetchone()
        species_names.append(res[1])
        species.append(res[2])
        Tc.append(res[3])
        Pc.append(res[4])
        Gj0.append(res[5])
        MW.append(res[6])
        HHV.append(res[7])

    conn.commit()
    conn.close()

    return species_names, species, Tc, Pc, Gj0, MW, HHV

def check_cas(species_cas):
    cas_to_add = []
    ind = []
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = 'SELECT Species_CAS FROM Critical_Properties WHERE Species_CAS = ?'
    for i, cas in enumerate(species_cas):
        parameters = (cas,)
        result = run_query(query, parameters).fetchone()
        print(result)
        if result == None:
            cas_to_add.append(cas)
            ind.append(i)
    conn.commit()
    conn.close()
    return cas_to_add, ind

