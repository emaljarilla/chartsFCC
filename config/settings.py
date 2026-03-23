""" Configuration file for CEPAIM dashboard"""

from pathlib import Path

#Rutas: Creamos unas varialbes que consideraremos constantes, para que si cambian las rutas solo tengas que venir a cambiarlas aqui
BASE_DIR =  Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
CEPAIM_CSV = DATA_DIR / "cepaim.csv"
SHAPEFILE_ZIP = DATA_DIR / "comunidad_autonoma.zip"

#colores institucionales si mañana cambian los colores institucionales o queremos reutilizar el codigo para otra organización solo debemos cambiar los colores de un sitio
COLORS = {
    'primary':'#9d2d80',
    'secondary':'#feda4c',
    'accent':'#1c467e',
    'light':'#96a9c4',
    'sex':{
        'Hombre':'#9d2d80',
        'Mujer':'#feda4c'
    },
    'vulnerability':{
        'Vulnerable':'#1c467e',
        'No Vulnerable':'#96a9c4'
    },
}

#grupos de edad
AGE_BINS=[0,15,29,39,49,59,120]
AGE_LABELS=['0-15','16-29','30-39','40-49','50-59','60 y más']

#Mapeo de Comunidades Autónomas
CCAA_MAPPING = {
    "Andalucía": "Andalucía",
    "Aragón": "Aragón",
    "Asturias": "Asturias",
    "Baleares": "Baleares",
    "Castilla la Mancha": "Castilla-La Mancha",
    "Castilla y León": "Castilla-León",
    "Cataluña": "Cataluña",
    "Cantabria": "Cantabria",
    "Ciudad de Ceuta": "Ceuta",
    "Comunidad de Madrid": "Madrid",
    "Comunidad Valenciana": "Comunidad Valenciana",
    "Galicia": "Galicia",
    "Extremadura": "Extremadura",
    "Islas Canarias": "Canarias",
    "La Rioja": "La Rioja",
    "Melilla": "Melilla",
    "Navarra": "Navarra",
    "País Vasco": "País Vasco",
    "Región de Murcia": "Murcia"
}

#configuración de página Streamlit
STREAMLIT_CONFIG={
    "page_title": "Dashboard CEPAIM",
    "layout":"wide",
    "initial_sidebar_state":"expanded"
}
