#Creamos un nuevo archivo que gestione las funciones de los graficos

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional
from config.settings import COLORS

def create_donut_chart(
  df:pd.DataFrame,
  column:str,
  title:str,
  color:Optional[dict]=None  
)->go.Figure:
    #creador generico, algo que podamos usar cada vez que queramos hacer un gráfico donut
    if color is None:
        color= COLORS['sex']
    conteo = df[column].value_counts().reset_index()
    conteo.columns = ['Label','Total']

    total = conteo['Total'].sum()
    conteo['Porcentaje']=(conteo['Total']/total*100).round(2)
    fig =go.Figure(
        data=[go.Pie(
            labels=conteo['Label'],
            values=conteo['Total'],
            hole=0.40,
            marker=dict(color=[color.get(l,COLORS['primary'])for l in conteo['Label']]),
            textinfo='label+percent',
            hovertemplate='%{label}<br>Total: %{value}<br>%{percent}'
        )]
    )
    
    fig.update_layout(
        title={'text':f'{title}<br><sup>Total: {total}</sup>','x':0.5},
        showlegend=False
    )
    return fig

def create_bar_chart(
    df: pd.DataFrame,
    x:str,
    y:str,
    color:Optional[str]=None,
    title:str="",
    orientation:str="v"
)->go.Figure:
    #creador generio de grafico de barras
    if orientation == 'h':
        fig = px.bar(df,y=y, x=x, color = color, orientation='h')
    else:
        fig = px.bar(df,y=y, x=x, color = color)
        
    fig.update_layout(
        title=title,
        template='plotly_white'
    )
    return fig
    