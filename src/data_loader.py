#data loading an processing module

import pandas as pd
import geopandas as gpd
import json
import zipfile
import os
from pathlib import Path
from typing import Tuple, Optional, List, Union
from config.settings import (
    CEPAIM_CSV, SHAPEFILE_ZIP, AGE_BINS, AGE_LABELS,CCAA_MAPPING
)

def load_csv(file_path: Union[str, Path])-> pd.DataFrame:
    #cargamos el csv pero gestionamos los posibles errores de carga, antes no se hacia
    try:
        df= pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV not found: {file_path}")#nos dice que no encuentra el fichero y nos dice donde lo busca
    except Exception as e:
        raise ValueError(f"Error loading CSV: {e}")#lo que nos dice que existe un error indeterminado y nos idica que tipo de error hay
    return df

def process_dates(df:pd.DataFrame,date_columns = ["f_nacimiento", "fecha"])-> pd.DataFrame:
    #convertimos las fechas con una validacion
    
    for col in date_columns:
        try:
            df[col]=pd.to_datetime(df[col], format="mixed")
        except Exception as e:
            raise ValueError(f"Invalid date format in {col}: {e}")
    return df

def calculate_age(df: pd.DataFrame)->pd.DataFrame:
    #calculamos la edad exacta considerando el mes y el día
    df['Edad']=df["fecha"].dt.year - df['f_nacimiento'].dt.year
    df['Edad']-=((df["fecha"].dt.month < df['f_nacimiento'].dt.month) | 
                ((df["fecha"].dt.month == df['f_nacimiento'].dt.month) &
                (df["fecha"].dt.day < df['f_nacimiento'].dt.day))).astype(int)
    return df

def create_age_groups(df:pd.DataFrame)->pd.DataFrame:
    #Creamos el grupo de categorias de edad
    df['grupo_etario']=pd.cut(
        df["Edad"],
        bins=AGE_BINS,
        labels=AGE_LABELS,
        right=True
    )
    return df

def map_sex(df: pd.DataFrame) -> pd.DataFrame:
    #Mapeo de sexo segun codigo
    df['Sexo_mapped']=df['sexo'].map({'H':'Hombre','M':'Mujer'})
    return df

def map_vulnerability(df: pd.DataFrame) -> pd.DataFrame:
    #Mapa de vulnerabilidades segun codigo
    def _map(val):
        if(str(val).strip().lower() in  ['si','sí','1','vulnerable','true','yes','y','ye']):
            return 'vulnerable'
        elif (str(val).strip().lower() in  ['no','0','no vulnerable','false']):
            return 'No vulnerable'
        else:
            return 'No definido'
    
    df['vulnerable_label']=df['vulnerable'].apply(_map)
    return df

def load_geodata()-> Tuple[dict,gpd.GeoDataFrame]:
    #cargamos el proceso de shapefile con cache para que no tarde tanto en cargar si se ha cargado antes
    extract_folder = Path("shapefile_cache")
    extract_folder.mkdir(exist_ok=True)
    
    with zipfile.ZipFile(SHAPEFILE_ZIP, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
        
    shp_file=[f for f in os.listdir(extract_folder) if f.endswith(".shp")][0]
    shp_path = extract_folder / shp_file
    gdf = gpd.read_file(shp_path)
    geojson = json.loads(gdf.to_json())
    
    return geojson ,gdf

def load_full_data()-> Tuple[pd.DataFrame,dict,gpd.GeoDataFrame]:
    #Funcion principal, carga todos los procesos
    df = load_csv(CEPAIM_CSV)
    df = process_dates(df)
    df = calculate_age(df)
    df = create_age_groups(df)
    df = map_sex(df)
    df = map_vulnerability(df)
    
    geojson,gdf=load_geodata()
    
    return df, geojson,gdf
    

""" Lo que estamos consiguiendo con es que cada bloque, cada funcion haga una sola cosa, donde la gestion de errores está mas definida y si nos dalla algo sabemos o tenemos mas facilidad de encontrar cual es quien falla.
Tambien con este modelo los test son mas faciles de implementar"""

