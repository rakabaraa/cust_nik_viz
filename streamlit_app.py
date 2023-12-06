import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout='wide')

# --- READ DATA ---
cust_merge = pd.read_pickle('data/customer_clean.pkl')
coord = pd.read_csv('data/coordinate.csv')

# --- ROW 1 ---
st.write('# Customer Demography Dashboard')
st.write("""A comprehensive view of the diverse tapestry that makes up our customer base.
          This dynamic visualization tool provides valuable insights into the demographics of our clientele,
          empowering you to make informed decisions and tailor strategies to better serve their needs.""")

# --- ROW 2 ---
col1, col2 = st.columns(2)

# --- INPUT SELECT 1 ---
cust_prov = cust_merge[['province', 'Spending_Score']]
cust_freq_prov = pd.crosstab(index=cust_prov['province'],
                             columns='Count',
                             colnames=[None]).reset_index()
cust_prov_grouped = cust_prov.groupby('province', observed=True).mean().reset_index()
cust_prov_grouped['Spending_Score'] = cust_prov_grouped['Spending_Score'].round(2)
cust_prov_merge = cust_freq_prov.merge(cust_prov_grouped, on='province')
df_map = cust_prov_merge.merge(coord, on='province')
df_map.columns = df_map.columns.str.replace("Spending_Score", "Average Spending Score")
df_map_melt = df_map.melt(id_vars=['province', 'longitude', 'latitude'])
size_select = col1.selectbox(label='Marker Size by:',
               options=df_map_melt['variable'].unique()
               )

# --- INPUT SELECT 2 ---
cust_gen = cust_merge[['generation', 'Spending_Score', 'Annual_Income']]
cust_gen_freq = pd.crosstab(cust_merge['generation'],
                            columns='Count',
                            colnames=[None]).reset_index()
cust_gen_grouped = cust_gen.groupby('generation', observed=True).mean().reset_index()
cust_gen_merge = cust_gen_freq.merge(cust_gen_grouped, on='generation')
cust_gen_merge['Spending_Score'] = cust_gen_merge['Spending_Score'].round(2)
cust_gen_merge.columns = cust_gen_merge.columns.str.replace("Spending_Score", "Average Spending Score")
cust_gen_merge.columns = cust_gen_merge.columns.str.replace("Annual_Income", "Average Annual Income")
df_gen = cust_gen_merge.melt(id_vars='generation')
gen_select = col2.selectbox(label='Show by:',
                            options=df_gen['variable'].unique())

# --- ROW 3 ---
col3, col4 = st.columns(2)

# --- MAP PLOT ---
# data
point_size = df_map[size_select]

# plot
plot_map = px.scatter_mapbox(data_frame=df_map, lat='latitude', lon='longitude',
                             mapbox_style='carto-positron', zoom=3,
                             size=point_size,
                             hover_name='province',
                             hover_data={'Count': True,
                                         'Average Spending Score': True,
                                         'latitude': False,
                                         'longitude': False})

col3.write('### Customer Info Based on Region')
col3.plotly_chart(plot_map, use_container_width=True)

# --- BAR PLOT 1 ---
# data
gen_info = cust_gen_merge[gen_select]

# plot
plot_gen = px.bar(cust_gen_merge, x='generation', y=gen_info, 
                   labels = {'generation' : 'Generation'})

col4.write(f'### Customer {gen_select} Based on Generation')
col4.plotly_chart(plot_gen, use_container_width=True)

# --- ROW 4 ---
st.divider()
col5, col6 = st.columns(2)

# --- INPUT SLIDER ---
input_slider = col5.slider(label='Select age range',
            min_value=cust_merge['age'].min(),
            max_value=cust_merge['age'].max(),
            value=[35,50])

min_slider = input_slider[0]
max_slider = input_slider[1]

# --- INPUT SELECT 3 ---
cust_prof = cust_merge[['Profession','Spending_Score', 'Annual_Income']]
cust_prof_freq = pd.crosstab(index=cust_prof['Profession'],
                             columns='Count',
                             colnames=[None]).reset_index()
cust_prof_grouped = cust_prof.groupby('Profession', observed=True).mean().reset_index()
cust_prof_merge = cust_prof_freq.merge(cust_prof_grouped, on='Profession')
cust_prof_merge['Spending_Score'] = cust_prof_merge['Spending_Score'].round(2)
cust_prof_merge.columns = cust_prof_merge.columns.str.replace("Spending_Score", "Average Spending Score")
cust_prof_merge.columns = cust_prof_merge.columns.str.replace("Annual_Income", "Average Annual Income")
df_prof = cust_prof_merge.melt(id_vars='Profession')
prof_select = col6.selectbox(label='Show By:',
                            options=df_prof['variable'].unique())

# --- ROW 5 ---
col7, col8 = st.columns(2)

# --- INPUT SELECT 4 ---
cust_age = cust_merge[cust_merge['age'].between(left=min_slider, right=max_slider)]
cust_gender = cust_age[['gender', 'Spending_Score']]
cust_gender_freq = pd.crosstab(index=cust_gender['gender'],
                               columns='Count',
                               colnames=[None])
cust_gender_grouped = cust_gender.groupby('gender', observed=True).mean().reset_index()
cust_gender_merge = cust_gender_freq.merge(cust_gender_grouped, on='gender')
cust_gender_merge['Spending_Score'] = cust_gender_merge['Spending_Score'].round(2)
cust_gender_merge.columns = cust_gender_merge.columns.str.replace("Spending_Score", "Average Spending Score")
df_gender = cust_gender_merge.melt(id_vars='gender')
gender_select = col7.selectbox(label='Show by:',
                            options=df_gender['variable'].unique())

# --- ROW 6 ---
col9, col10 = st.columns(2)

# --- BAR PLOT 2 ---
# data
gender_info = cust_gender_merge[gender_select]

# plot
gender_plot = px.bar(cust_gender_merge, 
                     x=gender_info, y='gender',
                     labels = {'gender': 'Gender'}
                               )

col9.write(f'### Customer {gender_select} Based on Gender, Age {min_slider} to {max_slider}')
col9.plotly_chart(gender_plot, use_container_width=True)

# --- BAR PLOT 3 ---
# data
prof_info = f'{prof_select}'

# plot
prof_plot = px.bar(cust_prof_merge.sort_values(by=prof_info, ascending=True), 
                     x=prof_info, y='Profession')

col10.write(f'### Customer {prof_select} Based on Profession')
col10.plotly_chart(prof_plot, use_container_width=True)

# --- ROW 7 ---
style_footer = """
<style>
footer:before{content:'This dashboard was developed using a set of dummy data as part of Learning by Building project in data science workshop titled "NIK Data Enrichment and Interactive Visualization" provided by algorit.ma.';
display:block;
position:relative;}
</style>
"""
st.markdown(style_footer, unsafe_allow_html=True)