import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from src.data_loader import load_full_data
from src.charts import create_donut_chart, create_bar_chart
from config.settings import STREAMLIT_CONFIG

st.set_page_config(
    page_title=STREAMLIT_CONFIG["page_title"],
    layout=STREAMLIT_CONFIG["layout"],
    initial_sidebar_state=STREAMLIT_CONFIG["initial_sidebar_state"]
)

st.title("Dashboard CEPAIM")
st.markdown("Análisis de participantes")

@st.cache_data
def get_data():
    return load_full_data()

try:
    df, geojson, gdf = get_data()
    
    st.sidebar.header("Filtros")
    
    sexo_filter = st.sidebar.multiselect(
        "Sexo",
        options=df["Sexo_mapped"].unique(),
        default=df["Sexo_mapped"].unique()
    )
    
    vulnerabilidad_filter = st.sidebar.multiselect(
        "Vulnerabilidad",
        options=df["vulnerable_label"].unique(),
        default=df["vulnerable_label"].unique()
    )
    
    comunidad_filter = st.sidebar.multiselect(
        "Comunidad Autónoma",
        options=sorted(df["comunidad"].dropna().unique()),
        default=sorted(df["comunidad"].dropna().unique())
    )
    
    area_filter = st.sidebar.multiselect(
        "Área",
        options=sorted(df["area"].dropna().unique()),
        default=sorted(df["area"].dropna().unique())
    )
    
    proyecto_filter = st.sidebar.multiselect(
        "Proyecto",
        options=sorted(df["id_proyecto"].unique()),
        default=sorted(df["id_proyecto"].unique())[:10]
    )
    
    centro_filter = st.sidebar.multiselect(
        "Centro",
        options=sorted(df["centro"].dropna().unique()),
        default=sorted(df["centro"].dropna().unique())[:10]
    )
    
    nacionalidades = sorted(df["nacionalidad"].dropna().unique())
    paises = sorted(df["pais_origen"].dropna().unique())
    años = sorted(df["año"].unique())
    meses_disponibles = sorted(df["mes_nombre"].unique())
    
    with st.sidebar.expander("Más filtros"):
        pais_filter = st.multiselect("País de Origen", paises, default=paises[:10])
        nac_filter = st.multiselect("Nacionalidad", nacionalidades, default=nacionalidades[:10])
        min_edad, max_edad = int(df["Edad"].min()), int(df["Edad"].max())
        edad_range = st.slider("Rango de Edad", min_edad, max_edad, (min_edad, max_edad))
        año_filter = st.multiselect("Año", años, default=años)
        trimestre_filter = st.multiselect("Trimestre", [1,2,3,4], default=[1,2,3,4])
        mes_filter = st.multiselect("Mes", meses_disponibles, default=meses_disponibles)
    
    df_filtered = df[
        (df["Sexo_mapped"].isin(sexo_filter)) &
        (df["vulnerable_label"].isin(vulnerabilidad_filter)) &
        (df["comunidad"].isin(comunidad_filter)) &
        (df["area"].isin(area_filter)) &
        (df["id_proyecto"].isin(proyecto_filter)) &
        (df["centro"].isin(centro_filter)) &
        (df["pais_origen"].isin(pais_filter)) &
        (df["nacionalidad"].isin(nac_filter)) &
        (df["Edad"] >= edad_range[0]) &
        (df["Edad"] <= edad_range[1]) &
        (df["año"].isin(año_filter)) &
        (df["trimestre"].isin(trimestre_filter)) &
        (df["mes_nombre"].isin(mes_filter))
    ]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Participantes", len(df_filtered))
    with col2:
        st.metric("Mujeres", len(df_filtered[df_filtered["Sexo_mapped"] == "Mujer"]))
    with col3:
        st.metric("Vulnerables", len(df_filtered[df_filtered["vulnerable_label"] == "Vulnerable"]))
    with col4:
        avg_edad = df_filtered["Edad"].mean()
        st.metric("Edad Media", f"{avg_edad:.1f} años")
    
    st.divider()
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        fig_sexo = create_donut_chart(
            df_filtered,
            "Sexo_mapped",
            "Distribución por Sexo"
        )
        st.plotly_chart(fig_sexo, use_container_width=True)
    
    with col_chart2:
        fig_vuln = create_donut_chart(
            df_filtered,
            "vulnerable_label",
            "Distribución por Vulnerabilidad",
            color={"Vulnerable": "#1c467e", "No vulnerable": "#96a9c4", "No definido": "#cccccc"}
        )
        st.plotly_chart(fig_vuln, use_container_width=True)
    
    st.divider()
    
    edad_counts = df_filtered["grupo_etario"].value_counts().reset_index()
    edad_counts.columns = ["Grupo Etario", "Total"]
    fig_edad = create_bar_chart(
        edad_counts,
        x="Grupo Etario",
        y="Total",
        title="Participantes por Grupo de Edad"
    )
    st.plotly_chart(fig_edad, use_container_width=True)
    
    st.divider()
    
    st.subheader("Análisis por Comunidad Autónoma")
    
    comundiad_counts = df_filtered["comunidad"].value_counts().reset_index()
    comundiad_counts.columns = ["Comunidad", "Total"]
    fig_comunidad = create_bar_chart(
        comundiad_counts,
        x="Total",
        y="Comunidad",
        orientation="h",
        title="Participantes por Comunidad Autónoma"
    )
    st.plotly_chart(fig_comunidad, use_container_width=True)
    
    st.divider()
    
    st.subheader("Evolución Temporal")
    
    col_time1, col_time2 = st.columns(2)
    
    with col_time1:
        año_counts = df_filtered["año"].value_counts().sort_index().reset_index()
        año_counts.columns = ["Año", "Total"]
        fig_año = create_bar_chart(
            año_counts,
            x="Año",
            y="Total",
            title="Participantes por Año"
        )
        st.plotly_chart(fig_año, use_container_width=True)
    
    with col_time2:
        trimestre_counts = df_filtered.groupby("trimestre").size().reset_index()
        trimestre_counts.columns = ["Trimestre", "Total"]
        trimestre_counts["Trimestre"] = trimestre_counts["Trimestre"].map({1:"Q1",2:"Q2",3:"Q3",4:"Q4"})
        fig_trim = create_bar_chart(
            trimestre_counts,
            x="Trimestre",
            y="Total",
            title="Participantes por Trimestre"
        )
        st.plotly_chart(fig_trim, use_container_width=True)

except Exception as e:
    st.error(f"Error al cargar datos: {e}")