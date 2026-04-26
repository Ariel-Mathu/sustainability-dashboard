import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Global Undernourishment Dashboard",
    page_icon="🌍",
    layout="wide"
)

# Title and introduction
st.title("🌍 Global Undernourishment Dashboard")
st.markdown("""
This dashboard explores the **prevalence of undernourishment** across the world 
from 2001 to 2023, using data from the **World Bank**.
Use the filters on the left to explore different countries and time periods.
""")

# Load the cleaned data
@st.cache_data
def load_data():
    df = pd.read_csv('data/cleaned/WB_undernourishment_cleaned.csv')
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Data")

# Year filter
years = sorted(df['Year'].unique())
selected_years = st.sidebar.slider(
    "Select Year Range",
    min_value=int(min(years)),
    max_value=int(max(years)),
    value=(2001, 2023)
)

# Country filter
countries = sorted(df['Country'].unique())
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=countries,
    default=["India", "Nigeria", "Ethiopia", "Bangladesh", "Kenya"]
)

# Filter the dataframe based on selections
df_filtered = df[
    (df['Year'] >= selected_years[0]) &
    (df['Year'] <= selected_years[1])
]

df_country = df_filtered[df_filtered['Country'].isin(selected_countries)]

# Row 1 - Line chart and Bar chart
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Undernourishment Trends Over Time")
    if len(selected_countries) > 0:
        fig_line = px.line(
            df_country,
            x='Year',
            y='Undernourishment_Pct',
            color='Country',
            title='Undernourishment % by Country Over Time',
            labels={'Undernourishment_Pct': 'Undernourishment (%)'}
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.warning("Please select at least one country from the sidebar.")

with col2:
    st.subheader("🏆 Top 10 Most Affected Countries")
    df_top10 = df_filtered.groupby('Country')['Undernourishment_Pct'].mean().reset_index()
    df_top10 = df_top10.sort_values('Undernourishment_Pct', ascending=False).head(10)
    fig_bar = px.bar(
        df_top10,
        x='Undernourishment_Pct',
        y='Country',
        orientation='h',
        title='Top 10 Countries by Average Undernourishment %',
        labels={'Undernourishment_Pct': 'Average Undernourishment (%)'},
        color='Undernourishment_Pct',
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# Row 2 - World map
st.subheader("🗺️ World Map of Undernourishment")

selected_year_map = st.slider(
    "Select Year for Map",
    min_value=int(min(years)),
    max_value=int(max(years)),
    value=2023
)

df_map = df[df['Year'] == selected_year_map]

fig_map = px.choropleth(
    df_map,
    locations='Country',
    locationmode='country names',
    color='Undernourishment_Pct',
    hover_name='Country',
    color_continuous_scale='Reds',
    title=f'Global Undernourishment in {selected_year_map}',
    labels={'Undernourishment_Pct': 'Undernourishment (%)'}
)
st.plotly_chart(fig_map, use_container_width=True)

# Row 3 - Data table
st.subheader("📋 Raw Data Table")
st.table(df_filtered.sort_values(['Year', 'Country']).head(50))

# Footer
st.markdown("---")
st.markdown("**Data Source:** World Bank — Prevalence of Undernourishment (% of Population)")