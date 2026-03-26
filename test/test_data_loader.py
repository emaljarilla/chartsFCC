import pytest
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go

from pathlib import Path
from src.data_loader import load_csv, process_dates, calculate_age, create_age_groups, map_sex, map_vulnerability,load_geodata, load_full_data
from config.settings import CEPAIM_CSV
from src.charts import create_bar_chart, create_donut_chart
# test 1
def test_load_csv_con_ruta_valida_devuelve_dataframe():
    """
    Cuando el archivo CSV existe y es valido. load_csv 
    debe devolver un objeto pandas DataFrame
    """
    #ACT: Llamar a la funcuin con la rura del CSV
    df = load_csv(CEPAIM_CSV)
    #El assert: verifica que el resulrtado es un DataFrame
    assert isinstance(df, pd.DataFrame)
# test 2 
def test_loaad_csv_con_ruta_invalida_file_not_found():
    '''cualdo el archivo no existe lanza una excepcion'''
    ruta_invalidad= "/ruta_invalida.py"
    #cargamos y verificamos que lanza la excepcion correcta
    with pytest.raises(FileNotFoundError):
        load_csv(ruta_invalidad)
# test 3
def test_load_csv_devuelve_columnas_esperadas():
    #primero debemos de cargar el fichero
    df =load_csv(CEPAIM_CSV)
    
    #creamos una lista con las columnas esperadas
    columnas_a_filtrar = ['f_nacimiento','fecha','sexo','nacionalidad','comunidad','vulnerable']
    for col in columnas_a_filtrar:
        assert col in df.columns, f"Columna '{col}' no encontrada"
# test 4
def test_load_csv_numero_de_filas():
      """El DataFrame tiene filas (no está vacío)."""
      df = load_csv(CEPAIM_CSV)
      assert len(df) > 0, "El CSV está vacío"
# test 5
def test_process_dates_convierte_a_date_time():
    df=load_csv(CEPAIM_CSV)
    df=process_dates(df,['f_nacimiento','fecha'])
    assert pd.api.types.is_datetime64_any_dtype(df['fecha'])
    assert pd.api.types.is_datetime64_any_dtype(df['f_nacimiento'])
# test 6
def test_process_dates_con_formato_invalido_lanza_error():
      """Si una fecha tiene formato inválido, lanza ValueError."""
      df_malo = pd.DataFrame({
          'Fecha de nacimiento': ['no-es-una-fecha'],
          'Fecha': ['18/03/2025']
      })
      with pytest.raises(ValueError):
          process_dates(df_malo)
# test 7
def test_calculate_age_cumplidos():
    df=pd.DataFrame({
        'f_nacimiento':['15/03/1990'],
        'fecha':['10/03/2025']
    })
    df['f_nacimiento']=pd.to_datetime(df['f_nacimiento'], format="mixed")
    df['fecha']=pd.to_datetime(df['fecha'], format="mixed")

    df=calculate_age(df)
    assert df['Edad'].iloc[0] == 35
# test 8
def test_calculate_age_cumple():
    df=pd.DataFrame({
        'f_nacimiento':['15/03/1990'],
        'fecha':['15/03/2025']
    })
    df['f_nacimiento']=pd.to_datetime(df['f_nacimiento'], format="mixed")
    df['fecha']=pd.to_datetime(df['fecha'], format="mixed")

    df=calculate_age(df)
    assert df['Edad'].iloc[0] == 35

# test 9
def test_calculate_age_no_cumple():
    df=pd.DataFrame({
        'f_nacimiento':['15/12/1990'],
        'fecha':['10/03/2025']
    })
    
    df['f_nacimiento']=pd.to_datetime(df['f_nacimiento'], format="mixed")
    df['fecha']=pd.to_datetime(df['fecha'], format="mixed")
    edad=df["fecha"].dt.year - df['f_nacimiento'].dt.year
    df=calculate_age(df)
    assert df['Edad'].iloc[0] != edad.iloc[0]
#test9.1
def test_calculate_age_multiples_personas():
    df=pd.DataFrame({
        'f_nacimiento':['15/12/1990','15/01/1990','15/12/1990','15/06/1990','15/07/1990'],
        'fecha':['15/12/2025','15/12/2025','15/01/2025','15/07/2025','15/05/2025']
    })
    df['f_nacimiento']=pd.to_datetime(df['f_nacimiento'], format="mixed")
    df['fecha']=pd.to_datetime(df['fecha'], format="mixed")
    df=calculate_age(df)
    assert df['Edad'].iloc[0] == 35
    assert df['Edad'].iloc[1] == 35
    assert df['Edad'].iloc[2] < 35
    assert df['Edad'].iloc[2] == 34
    assert df['Edad'].iloc[3] == 35
    assert df['Edad'].iloc[4] < 35
    assert df['Edad'].iloc[4] == 34


# test 10
def test_create_age_groups_asigna_bines_correctamente():
    df=pd.DataFrame({'Edad':[0,5,8,26,31,41,55,90]})
   
    df = create_age_groups(df)
    # Verificar que cada persona está en el grupo correcto  
    assert df.loc[df['Edad'] == 5, 'grupo_etario'].iloc[0] == '0-15'
    assert df.loc[df['Edad'] == 26, 'grupo_etario'].iloc[0] == '16-29'
    assert df.loc[df['Edad'] == 31, 'grupo_etario'].iloc[0] == '30-39'
    assert df.loc[df['Edad'] == 41, 'grupo_etario'].iloc[0] == '40-49'
    assert df.loc[df['Edad'] == 55, 'grupo_etario'].iloc[0] == '50-59'
    assert df.loc[df['Edad'] == 90, 'grupo_etario'].iloc[0] == '60 y más'

#text 10.1
def test_create_age_groups_60_mas_incluye_todos():
    df=pd.DataFrame({'Edad':[60,70,80,90,100,120,130,160]})
   
    df = create_age_groups(df)
    for edad in [60, 70, 80, 90, 100, 120]:
        grupo = df.loc[df['Edad'] == edad, 'grupo_etario'].iloc[0]
        assert grupo == '60 y más', f"Edad {edad} debería estar en '60 y más'"
 # test 11
def test_map_sex_h_devuelve_hombre():
    df=pd.DataFrame({'sexo':['H']})
    resultado = map_sex(df)
    assert resultado['Sexo_mapped'].iloc[0]=='Hombre'

 # test 12
def test_map_sex_h_devuelve_mujer():
    df=pd.DataFrame({'sexo':['M']})
    resultado = map_sex(df)
    assert resultado['Sexo_mapped'].iloc[0]=='Mujer'

# test 13
def test_map_sex_h_devuelve_multiples():
    df=pd.DataFrame({'sexo':['H','H','M','H','M','H','H','H','M','M','H','M','M','H']})
    resultado = map_sex(df)
    assert resultado['Sexo_mapped'].iloc[0]=='Hombre'
    assert resultado['Sexo_mapped'].iloc[1]=='Hombre'
    assert resultado['Sexo_mapped'].iloc[2]=='Mujer'
    assert resultado['Sexo_mapped'].iloc[3]=='Hombre'
    assert resultado['Sexo_mapped'].iloc[4]=='Mujer'
    assert resultado['Sexo_mapped'].iloc[5]=='Hombre'
    assert resultado['Sexo_mapped'].iloc[6]=='Hombre'
    assert resultado['Sexo_mapped'].iloc[7]=='Hombre'
    assert resultado['Sexo_mapped'].iloc[8]=='Mujer'
    assert resultado['Sexo_mapped'].iloc[9]=='Mujer'
    assert resultado['Sexo_mapped'].iloc[10]=='Hombre'
    assert resultado['Sexo_mapped'].iloc[11]=='Mujer'
    assert resultado['Sexo_mapped'].iloc[12]=='Mujer'
    assert resultado['Sexo_mapped'].iloc[13]=='Hombre'

#test 14
def test_map_vulnerability_todas_las_variantes_de_si():
    df=pd.DataFrame({'vulnerable':['si']})
    resultado=map_vulnerability(df)
    assert resultado['vulnerable_label'].iloc[0]=="vulnerable"
#test 15
def test_map_vulnerability_todas_las_variantes_de_no():
    df=pd.DataFrame({'vulnerable':['no']})
    resultado=map_vulnerability(df)
    assert resultado['vulnerable_label'].iloc[0]=="No vulnerable"
#test 14
def test_map_vulnerability_todas_las_variantes():
    df=pd.DataFrame({'vulnerable':['0','is','nO','false','fAlSe','1']})
    resultado=map_vulnerability(df)
    assert resultado['vulnerable_label'].iloc[0]=='No vulnerable'
    assert resultado['vulnerable_label'].iloc[1]=='No definido'
    assert resultado['vulnerable_label'].iloc[2]=='No vulnerable'
    assert resultado['vulnerable_label'].iloc[3]=='No vulnerable'
    assert resultado['vulnerable_label'].iloc[4]=='No vulnerable'
    assert resultado['vulnerable_label'].iloc[5]=="vulnerable"
def test_map_vulnerability_con_espacios():
    df=pd.DataFrame({'vulnerable':['0 ',' is',' nO ','     false ','  fAlSe         ','   1                                 ']})
    resultado=map_vulnerability(df)
    assert resultado['vulnerable_label'].iloc[0]=='No vulnerable'
    assert resultado['vulnerable_label'].iloc[1]=='No definido'
    assert resultado['vulnerable_label'].iloc[2]=='No vulnerable'
    assert resultado['vulnerable_label'].iloc[3]=='No vulnerable'
    assert resultado['vulnerable_label'].iloc[4]=='No vulnerable'
    assert resultado['vulnerable_label'].iloc[5]=="vulnerable"
#test 15
def test_load_geodata_devuelve_dos_elementos():
    geojson, gdf = load_geodata()
    assert isinstance(geojson, dict)
    assert isinstance(gdf, gpd.GeoDataFrame)

#test 16
def test_load_geodata_geojson_tiene_features():
    geojson, gdf = load_geodata()
    assert 'features' in geojson
    assert len(geojson['features']) > 0
 
#test 17
def test_load_full_data_devuelve_tres_elemenos():
    df, geojson, gdf = load_full_data()
    assert isinstance(df, pd.DataFrame) 
    assert isinstance(geojson, dict)
    assert isinstance(gdf, gpd.GeoDataFrame)
#test 18
def test_load_geodata_geojson_tiene_geometrias():
    geojson, gdf = load_geodata()
    assert 'geometry' in gdf
    assert gdf.geometry.iloc[0] is not None
#test 19
def test_load_full_data_crea_columnas_derivadas():
    geojson, gdf = load_geodata()
    
#test 20

#test 21

#test 22

