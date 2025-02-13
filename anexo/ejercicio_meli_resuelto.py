#!/usr/bin/env python
'''
SQL ORM [Python]
Ejercicios de profundización Meli
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
En este ejemplo se utiliza además de SQL ORM
corrutinas para acelerar el tiempo de procesamiento
Este tema excede a lo visto en clase, pero puede que al alumno
le interese profundizar en este campo.
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.1"

import csv
import requests
import time

# SqlAlchemy
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Creo el motor (engine) de la base de datos
engine = sqlalchemy.create_engine("sqlite:///articulos_mercadolibre.db")
base = declarative_base()


def persist(data):
    '''Persistir en la base de datos el articulo'''    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    articulo = Articulo(id=data['id'], site_id=data['site_id'], title=data['title'], price=data['price'],
                            currency_id=data['currency_id'], initial_quantity=data['initial_quantity'],
                            available_quantity=data['available_quantity'], sold_quantity=data['sold_quantity'])
    
    session.add(articulo)
    session.commit()


def fetch(url):
    '''Consultar los datos en la URL'''
    try:
        data = requests.get(url).json()
        body_data = data[0]['body']
        persist(body_data)
    except Exception as e:
        #print("request Excep", e)
        return


class Articulo(base):
    __tablename__ = 'articulo'
    id = Column(String, primary_key=True, autoincrement=False)
    site_id = Column(String)
    title = Column(String)
    price = Column(Integer)
    currency_id = Column(String)
    initial_quantity = Column(Integer)
    available_quantity = Column(Integer)
    sold_quantity = Column(Integer)

    def __repr__(self):
        return f'Articulo\nId: {self.id}\nSite id: {self.site_id}\nTitle: {self.title}\
                 \nPrice: {self.price}\nCurrency id: {self.currency_id},\nInitial Quantity: {self.initial_quantity}\
                 \nAvailable Quantity: {self.initial_quantity}\nSold Quantity: {self.sold_quantity}'


def create_schema():
    base.metadata.drop_all(engine)
    base.metadata.create_all(engine)


def fill():

    t1 = time.time()
    with open('meli_technical_challenge_data.csv', 'r') as f:
        data = list(csv.DictReader(f))

        for x in data:
            item = x['site'] + x['id']

            url = 'https://api.mercadolibre.com/items?ids={}'.format(item)

            fetch(url)

    t2 = time.time()
    print("Tiempo de procesamiento:", t2-t1)

if __name__ == "__main__":
  # Crear DB
  create_schema()

  # Completar la DB, lanzar rutinas asyncronicas
  fill()
  
