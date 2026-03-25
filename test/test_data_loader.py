import pytest
import pandas as pd
import geopandas as gpd
from pathlib import Path

from src.data_loader import load_csv, process_dates, calculate_age, create_age_groups, map_sex, map_vulnerability,load_geodata
from config.settings import CEPAIM_CSV
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
    df=pd.DataFrame({'Vulnerable':['si']})
    resultado=map_vulnerability(df)
    assert resultado['vulnerable_label'].iloc[0]=="Vulnerable"
#test 15
def test_map_vulnerability_todas_las_variantes_de_no():
    df=pd.DataFrame({'Vulnerable':['no']})
    resultado=map_vulnerability(df)
    assert resultado['vulnerable_label'].iloc[0]=="No vulnerable"
#test 14
def test_map_vulnerability_todas_las_variantes():
    df=pd.DataFrame({'Vulnerable':['0','is','nO','false','fAlSe','1']})
    resultado=map_vulnerability(df)
    assert resultado['vulnerable_label'].iloc[0]=='No vulnerable'
    assert resultado['vulnerable_label'].iloc[1]=='No definido'
    assert resultado['vulnerable_label'].iloc[2]=='No vulnerable'
    assert resultado['vulnerable_label'].iloc[3]=='No vulnerable'
    assert resultado['vulnerable_label'].iloc[4]=='No vulnerable'
    assert resultado['vulnerable_label'].iloc[5]=="Vulnerable"

#test 15
def test_load_geodatos():
    geojson, gdf = load_geodata()
    assert isinstance(geojson, dict)
    assert isinstance(gdf, gpd.GeoDataFrame)

    