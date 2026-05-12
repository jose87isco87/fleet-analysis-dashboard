import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Análisis Integral de Flota", layout="wide")

# Datos completos extraídos del reporte oficial (Única fuente de verdad)
datos_completos = [
    # Región Chorotega
    {"Región": "Chorotega", "Área": "ALTA", "Cuadrillas": 8, "Carros Actuales": 13, "Personas": 26},
    {"Región": "Chorotega", "Área": "P y M", "Cuadrillas": 7, "Carros Actuales": 9, "Personas": 21},
    {"Región": "Chorotega", "Área": "Líneas", "Cuadrillas": 6, "Carros Actuales": 16, "Personas": 38},
    {"Región": "Chorotega", "Área": "OC", "Cuadrillas": 3, "Carros Actuales": 5, "Personas": 15},
    {"Región": "Chorotega", "Área": "OP", "Cuadrillas": 4, "Carros Actuales": 5, "Personas": 7}, 
    {"Región": "Chorotega", "Área": "Salud", "Cuadrillas": 0, "Carros Actuales": 2, "Personas": 2},
    
    # Región Central
    {"Región": "Central", "Área": "ALTA", "Cuadrillas": 6, "Carros Actuales": 10, "Personas": 26},
    {"Región": "Central", "Área": "P y M", "Cuadrillas": 6, "Carros Actuales": 9, "Personas": 20},
    {"Región": "Central", "Área": "Líneas", "Cuadrillas": 5, "Carros Actuales": 14, "Personas": 42},
    {"Región": "Central", "Área": "OC", "Cuadrillas": 3, "Carros Actuales": 5, "Personas": 16},
    {"Región": "Central", "Área": "OP", "Cuadrillas": 4, "Carros Actuales": 4, "Personas": 7}, 
    {"Región": "Central", "Área": "Salud", "Cuadrillas": 0, "Carros Actuales": 0, "Personas": 0},
    
    # Región Huetar
    {"Región": "Huetar", "Área": "Alta", "Cuadrillas": 7, "Carros Actuales": 13, "Personas": 22},
    {"Región": "Huetar", "Área": "P y M", "Cuadrillas": 6, "Carros Actuales": 10, "Personas": 22},
    {"Región": "Huetar", "Área": "Línea", "Cuadrillas": 6, "Carros Actuales": 18, "Personas": 40},
    {"Región": "Huetar", "Área": "OC", "Cuadrillas": 3, "Carros Actuales": 6, "Personas": 9},
    {"Región": "Huetar", "Área": "OP", "Cuadrillas": 0, "Carros Actuales": 2, "Personas": 5},
    
    # Región GDO
    {"Región": "GDO", "Área": "Piom", "Cuadrillas": 0, "Carros Actuales": 0, "Personas": 11},
    {"Región": "GDO", "Área": "G Active", "Cuadrillas": 0, "Carros Actuales": 0, "Personas": 16},
    {"Región": "GDO", "Área": "DR TOC", "Cuadrillas": 0, "Carros Actuales": 0, "Personas": 13},
    {"Región": "GDO", "Área": "Pool", "Cuadrillas": 0, "Carros Actuales": 4, "Personas": 0},
    {"Región": "GDO", "Área": "Limat", "Cuadrillas": 7, "Carros Actuales": 10, "Personas": 32},
    {"Región": "GDO", "Área": "Matas", "Cuadrillas": 0, "Carros Actuales": 10, "Personas": 23},
    {"Región": "GDO", "Área": "Rigos", "Cuadrillas": 0, "Carros Actuales": 6, "Personas": 12},
    {"Región": "GDO", "Área": "Sala Contr", "Cuadrillas": 0, "Carros Actuales": 0, "Personas": 26},
    
    # Gestión 
    {"Región": "Gestión", "Área": "Única", "Cuadrillas": 0, "Carros Actuales": 5, "Personas": 53}
]

df_master = pd.DataFrame(datos_completos)

# Diccionario histórico de solicitudes regionales
solicitudes_regionales = {
    "Chorotega": 16, "Central": 20, "Huetar": 21, "GDO": 11, "Gestión": 0
}

st.title("Sistema de Análisis de Flota Vehicular")

# Crear pestañas para separar las vistas
tab1, tab2 = st.tabs(["📊 Visión General (Por Región)", "🔎 Análisis Detallado (Por Área y Cuadrilla)"])

# ==========================================
# PESTAÑA 1: VISIÓN GENERAL POR REGIÓN
# ==========================================
with tab1:
    st.header("Análisis Macro: Disponibilidad de Vehículos por Persona")
    
    # Agrupar los datos detallados a nivel regional
    df_region = df_master.groupby("Región").agg({
        "Carros Actuales": "sum",
        "Personas": "sum"
    }).reset_index()
    
    # Ordenar para mantener consistencia
    df_region["Orden"] = df_region["Región"].map({"Chorotega":1, "Central":2, "Huetar":3, "GDO":4, "Gestión":5})
    df_region = df_region.sort_values("Orden").drop("Orden", axis=1)

    col_input_reg, col_data_reg = st.columns([1, 3])
    
    with col_input_reg:
        st.subheader("Asignación Regional")
        st.markdown("Ajuste los vehículos a comprar:")
        nuevos_regionales = []
        for index, row in df_region.iterrows():
            region = row["Región"]
            solicitados = solicitudes_regionales.get(region, 0)
            # El parámetro 'key' evita que los sliders de diferentes pestañas se confundan
            val = st.slider(f"{region} (Req: {solicitados})", 0, 40, solicitados, key=f"reg_slider_{region}")
            nuevos_regionales.append(val)
            
    # Cálculos Regionales
    df_region["Nuevos Asignados"] = nuevos_regionales
    df_region["Total Carros (Proyectado)"] = df_region["Carros Actuales"] + df_region["Nuevos Asignados"]
    df_region["Personas por Carro (Actual)"] = round(df_region["Personas"] / df_region["Carros Actuales"], 2)
    df_region["Personas por Carro (Proyectado)"] = round(df_region["Personas"] / df_region["Total Carros (Proyectado)"], 2)

    with col_data_reg:
        st.subheader("Estado Consolidado")
        st.dataframe(df_region.style.format(precision=2), width="stretch")

    # Gráficos Regionales
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        fig1 = px.bar(df_region, x="Región", y=["Carros Actuales", "Nuevos Asignados"], title="Crecimiento de Flota (Consolidado)", barmode="stack", color_discrete_sequence=["#1f77b4", "#2ca02c"])
        st.plotly_chart(fig1, width="stretch")
    with col_chart2:
        fig2 = px.bar(df_region, x="Región", y=["Personas por Carro (Actual)", "Personas por Carro (Proyectado)"], title="Impacto: Personas por Vehículo", barmode="group", color_discrete_sequence=["#ff7f0e", "#17becf"])
        st.plotly_chart(fig2, width="stretch")


# ==========================================
# PESTAÑA 2: ANÁLISIS DETALLADO POR ÁREA
# ==========================================
with tab2:
    st.header("Análisis Micro: Disponibilidad de Vehículos por Cuadrilla")
    
    region_seleccionada = st.selectbox("Seleccione la Región a analizar detalladamente:", df_master["Región"].unique())
    df_filtrado = df_master[df_master["Región"] == region_seleccionada].copy()
    
    col_input_area, col_data_area = st.columns([1, 3])
    
    with col_input_area:
        st.subheader(f"Asignación Interna: {region_seleccionada}")
        
        # --- NUEVO INDICADOR DE PRESUPUESTO ---
        coches_solicitados = solicitudes_regionales.get(region_seleccionada, 0)
        st.info(f"🎯 **Meta de la Región:** {coches_solicitados} vehículos solicitados en total.")
        # --------------------------------------

        nuevos_asignados_area = []
        for index, row in df_filtrado.iterrows():
            area = row['Área']
            actuales = row['Carros Actuales']
            val = st.slider(f"Área {area} (Actual: {actuales})", 0, 15, 0, key=f"area_slider_{region_seleccionada}_{area}")
            nuevos_asignados_area.append(val)
            
        # --- NUEVO SEGUIMIENTO DINÁMICO ---
        total_asignado = sum(nuevos_asignados_area)
        if total_asignado > coches_solicitados:
            st.error(f"⚠️ Límite excedido: Ha asignado {total_asignado} de {coches_solicitados} vehículos.")
        elif total_asignado < coches_solicitados:
            st.warning(f"⏳ Faltan por asignar: {coches_solicitados - total_asignado} vehículos.")
        else:
            st.success(f"✅ Distribución completa: {total_asignado} de {coches_solicitados} vehículos asignados.")
        # ----------------------------------
            
    # Cálculos por Área
    df_filtrado["Nuevos Asignados"] = nuevos_asignados_area
    df_filtrado["Total Carros (Proyectado)"] = df_filtrado["Carros Actuales"] + df_filtrado["Nuevos Asignados"]

    def calcular_ratio_cuadrilla(carros, cuadrillas):
        return round(carros / cuadrillas, 2) if cuadrillas > 0 else None

    df_filtrado["Carros por Cuadrilla (Actual)"] = df_filtrado.apply(lambda x: calcular_ratio_cuadrilla(x["Carros Actuales"], x["Cuadrillas"]), axis=1)
    df_filtrado["Carros por Cuadrilla (Proyectado)"] = df_filtrado.apply(lambda x: calcular_ratio_cuadrilla(x["Total Carros (Proyectado)"], x["Cuadrillas"]), axis=1)

    with col_data_area:
        st.subheader("Estado Operativo por Área")
        st.dataframe(df_filtrado.style.format(precision=2, na_rep="-"), width="stretch")
        
    # Gráficos por Área
    col_chart3, col_chart4 = st.columns(2)
    with col_chart3:
        fig3 = px.bar(df_filtrado, x="Área", y=["Carros Actuales", "Nuevos Asignados"], title=f"Crecimiento de Flota en {region_seleccionada}", barmode="stack", color_discrete_sequence=["#1f77b4", "#2ca02c"])
        st.plotly_chart(fig3, width="stretch")
    with col_chart4:
        df_cuadrillas = df_filtrado[df_filtrado["Cuadrillas"] > 0]
        if not df_cuadrillas.empty:
            fig4 = px.bar(df_cuadrillas, x="Área", y=["Carros por Cuadrilla (Actual)", "Carros por Cuadrilla (Proyectado)"], title="Operatividad: Vehículos por Cuadrilla", barmode="group", color_discrete_sequence=["#ff7f0e", "#17becf"])
            fig4.add_hline(y=1.0, line_dash="dot", annotation_text="Meta: 1 Vehículo/Cuadrilla", line_color="red")
            st.plotly_chart(fig4, width="stretch")
        else:
            st.info("No hay cuadrillas registradas en esta vista para calcular operatividad.")