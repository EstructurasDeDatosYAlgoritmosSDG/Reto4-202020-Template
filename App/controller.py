"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """

import config as cf
from App import model
import csv
import os
from DISClib.ADT import stack
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def init():
    """
    Llama la funcion de inicializacion del modelo.
    """
    analyzer = model.newAnalyzer()

    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadTrips(citybike):
    principio = 0
    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('\nCargando archivo: ' + filename)
            num = loadFile(citybike, filename, principio)
            principio = principio + num[1]
    return citybike, principio

def loadFile(citybike, tripfile, principio):
    tripfile = cf.data_dir + tripfile
    input_file = csv.DictReader(open(tripfile,encoding="utf-8"), delimiter=",")
    numero = principio
    for trip in input_file:
        model.addTrip(citybike, trip)
        numero += 1
    return citybike, numero

def addStationGraph(citybike):
    return model.addStationGraph(citybike)

    
    

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________

def totalStops(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStops(analyzer)


def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)

def cantidad_componentes_fconectados(graph):
    cantidad = model.numSCC(graph['conecciones'])
    return cantidad

def pertenecen_al_mismo_cluster(graph, estacion1, estacion2):
    si = model.sameCC(graph['conecciones'],estacion1,estacion2)
    return si

def recomendar_ruta(citybike, rango):
    ruta = model.recomendar_ruta(citybike, rango)
    if ruta != '':
        estaciones_en_ruta = lt.newList()
        i = 1
        while i <= stack.size(ruta):
            camino = stack.pop(ruta)
            vertexA = camino['vertexA']
            vertexB = camino['vertexB']
            lt.addLast(estaciones_en_ruta,vertexA)
            lt.addLast(estaciones_en_ruta,vertexB)
            i += 1
        return estaciones_en_ruta

def ruta_turistica_resistencia(citybike, tiempo, id):
    return model.ruta_turistica_resistencia(citybike,tiempo,id)

def ruta_interes_turistico(citybike, longitud_origen, latitud_origen, longitud_destino, latitud_destino):
    camino = model.ruta_interes_turistico(citybike, longitud_origen, latitud_origen, longitud_destino, latitud_destino)
    if not isinstance(camino, str):
        tiempo = 0
        iterador = it.newIterator(camino)
        while it.hasNext(iterador):
            cam = it.next(iterador)
            peso = cam['weight']
            tiempo += peso
        return camino, tiempo
    return camino
  
def conocerEstacionesCriticas(citybike):
    lista = model.EstacionesCriticas(citybike)
    return lista

def identificar_bicicleta(citybike, bikeid, fecha):
    return model.identificar_bicicleta(citybike, bikeid, fecha)

def identificar_estaciones_publicidad(citybike, rango):
    return model.identificar_estaciones_publicidad(citybike, rango)