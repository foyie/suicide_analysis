import plotly.express as px
import pandas as pd
import streamlit as st
import altair as alt 
import plost
from streamlit_lottie import st_lottie
import json
import requests 
import time

my_bar = st.progress(0)

for percent_complete in range(100):
    time.sleep(0.001)
    my_bar.progress(percent_complete + 1)


st.title('🌎Suicide rate over Continents..')
# with st.spinner('Wait for it...'):
#     time.sleep(2)
    
df=pd.read_csv('countries.csv')
with st.sidebar:
        st.sidebar.header('`Suicide over continents`')
        
        st.subheader("These charts show the suicide rates over continents with respect to age,gender and generations ") 

        def load_lottieurl(url: str):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()

        lottie_hello = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_DKixY1wiMx.json")
        st_lottie(
            lottie_hello,
            speed=1,
            reverse=False,
            loop=True,
            quality="low", # medium ; high
            #renderer=None, # canvas
            height=400,
            width=300,
            key=None,
        )
        
        st.sidebar.markdown('''
---
*Created with* ❤️ by [Foyie](https://github.com/foyie).

''')

tab1, tab2 = st.tabs(["Bar chart",'Map'])

with tab1:
    st.header('Suicides by Continents and **Age**')
    st.subheader('`1985-2016`')
    # st.header('This is a header')
    
    data_age=pd.read_csv('age_conti.csv')
    colors = ["#c26b9c","#78b2de",'#88e3af',"#ffa58c",'#9f88e3','#5f6fb0']
    #colors=['#FF9AA2','#FFB7B2','#FFDAC1','#E2F0CB','#B5EAD7','#C7CEEA']
    hover = alt.selection_single(fields=['Suicides/100kPop'],
                    nearest=True,
                    
                    on="mouseover",
                    )   
    age_chart = (alt.Chart(data_age).mark_bar().encode(
    alt.Column('continent'), alt.X('Age'),
    alt.Y('Suicides/100kPop',axis=alt.Axis(grid=True)), 
    #alt.Color('Age'),
    alt.Color('Age',scale=alt.Scale(scheme='purplered')),
    opacity=alt.condition(hover, alt.value(1), alt.value(0.8)),
        
    tooltip=[
                            alt.Tooltip("Age", title="Age"),
                            alt.Tooltip("continent", title="continent"),
                            alt.Tooltip("Suicides/100kPop", title="Suicides/100kPop"),
                        ]).interactive().add_selection(hover)
                .configure_range(
        category=alt.RangeScheme(colors)
    ))

    st.altair_chart(age_chart)

    
    col1, col2 = st.columns([7,3])
    
    with col1:
        st.subheader('''Suicides by Continents and *Age*''')
        st.subheader('`1985-2016`')
        
        #st.subheader("Gender")    
        data_gend=pd.read_csv('gend_conti.csv')
        colors = ["#c26b9c","#78b2de",'#88e3af',"#ffa58c",'#9f88e3','#5f6fb0']

        gp_chart = (alt.Chart(data_gend).mark_bar().encode(
        alt.Column('continent'), alt.X('Gender'),
        alt.Y('Suicides/100kPop',axis=alt.Axis(grid=True)), 
        #alt.Color('Gender'),
        alt.Color('Gender',scale=alt.Scale(scheme='greenblue'), legend=alt.Legend(title="Age",orient='bottom')),
        opacity=alt.condition(hover, alt.value(1), alt.value(0.8)),
            
        tooltip=[
                                alt.Tooltip("Gender", title="Gender"),
                                alt.Tooltip("continent", title="continent"),
                                alt.Tooltip("Suicides/100kPop", title="Suicides/100kPop"),
                            ]).interactive().add_selection(hover)
            #         .configure_range(
            # category=alt.RangeScheme(colors))
        )

        st.altair_chart(gp_chart)
        
    with col2:
        data_conti=pd.read_csv('value_continents.csv')
        st.subheader('''Suicide rate over continents''')  
        plost.pie_chart(
        data=data_conti,
        theta="Suicides/100kPop",
        color=('continent'),
        height=400,
        width=400,
        legend='bottom',
         
        use_container_width=False)

        
                
with tab2:
    st.header('''Suicide rates shown on map with respect to `continents` ''')
    merge_conti=pd.read_csv('continents.csv')
    f_conti=px.choropleth(merge_conti,
                locationmode='country names',
                locations=merge_conti['Country'],
                # scope='world',
                color_continuous_scale="PuRd",
                height=500,
                width=1200,
                basemap_visible=True,

                hover_name=merge_conti['continent'],
                hover_data=['Suicides/100kPop','Country'],
                color=merge_conti['Suicides/100kPop'])
    f_conti.update_layout(margin={"r":0,"t":0,"l":0,"b":0},hoverlabel=dict(bgcolor=px.colors.sequential.PuRd[8]))
    f_conti.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations",
               )
    st.plotly_chart(f_conti,use_container_width=False)
        

