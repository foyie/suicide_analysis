import streamlit as st
import pandas as pd
import plost
import altair as alt 
from altair import Chart, X, Y, Axis, SortField, OpacityValue
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import json
import requests 
import time
from PIL import Image

image = Image.open('suicide.png')

st.image(image, caption='''Data Analysis''',width=100)

st.title("🌏Worldwide Suicides")
with st.spinner('Wait for it...'):
    time.sleep(4)

    
data=pd.read_csv('filt_data.csv')


with st.sidebar:
        st.sidebar.header("`Select a page above.`")
        st.sidebar.warning('`Suicide Data Analyis`')
        st.sidebar.markdown('''Mental health is once of the least talked about health hazards. Every year since a long time we loose so 
                            many individuals to suicides. This is a detailed analysis of suicide rates all over the world. Hopefully this analysis 
                            articulates the fact that suicide needs to be taken seriously and spreads mental health awareness.
                            ''')
        
       
        def load_lottieurl(url: str):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()

        lottie_hello = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_xr43alca.json")
        st_lottie(
            lottie_hello,
            speed=1,
            reverse=False,
            loop=True,
            quality="low", # medium ; high
            #renderer=None, # canvas
            height=300,
            width=300,
            key=None,
        )
        st.sidebar.markdown('''
---
*Created with* ❤️ by [Foyie](https://github.com/foyie).

''')
        

tab1, tab2, tab3 = st.tabs(["By age", "By Gender","World"])
               
with tab1:
    st.subheader('*Suicide rate with respect to `age`*')
    
    data_age1=data.groupby(["Year","Age"]).sum()
    data_age1=data_age1.reset_index()
    data_age1=data_age1.drop(['Suicides/100kPop', 'GdpPerCapitalMoney'],axis=1)
    data_age1['Suicides/100kPop']=(data_age1['SuicidesNo']/data_age1['Population'])*100000
    source=data_age1


    def get_chart(data):
        hover = alt.selection_single(
            fields=["Year",'Age'],
            nearest=True,
            on="mouseover",
            empty="none",
            
        )
        
        lines = (
            alt.Chart(data, title="Line chart")
            .mark_line(size=3)
            .encode(
                x=alt.X("Year",title='Year'),
                y=alt.Y("Suicides/100kPop",title='Suicide Rates',scale=alt.Scale(zero=False)),
                color=alt.Color('Age', legend=alt.Legend(title="Age",orient='bottom')),
                
                
                        
        ))
                

        points = lines.transform_filter(hover).mark_square(size=100)
        
        tooltips = (
            alt.Chart(data)
            .mark_rule(size=3,color='#628c43')
            .encode(
                x="Year",
                y="Suicides/100kPop",
                color='Age',
                        
                
                opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
                tooltip=[
                    alt.Tooltip("Year", title="year"),
                    alt.Tooltip("Age", title="Age"),
                    alt.Tooltip("Suicides/100kPop", title="Suicides/100kPop"),
                ],
            )
            .add_selection(hover)
        )
        return (lines+points+tooltips).interactive().properties(
        width=1000,
        height=600
    )

    chart = get_chart(source)
    # alt.renderers.enable('altair_viewer')
    st.altair_chart(chart, use_container_width=False)
    
    data_age2=data.groupby(['Age']).sum()
    data_age2=data_age2.reset_index()
    data_age2=data_age2.drop(['Suicides/100kPop', 'GdpPerCapitalMoney','Year'],axis=1)
    data_age2['Suicides/100kPop']=(data_age2['SuicidesNo']/data_age2['Population'])*100000

        
    st.markdown('### Donut chart')
    plost.donut_chart(
    data=data_age2,
    theta="Suicides/100kPop",
    color=('Age'),
    legend='right', 
    height=600,
    width=600,
    use_container_width=True)
                
            
with tab2:
    st.subheader('*Suicide rate with respect to `Gender`*')    
    data_gender1=data.groupby(["Year","Gender"]).sum()
    data_gender1=data_gender1.reset_index()
    data_gender1=data_gender1.drop(['Suicides/100kPop', 'GdpPerCapitalMoney'],axis=1)
    data_gender1['Suicides/100kPop']=(data_gender1['SuicidesNo']/data_gender1['Population'])*100000
    source2=data_gender1


    def get_chart(data):
        hover = alt.selection_single(
            fields=["Year",'Gender'],
            nearest=True,
            on="mouseover",
            empty="none",
            
        )
        
        lines = (
            alt.Chart(data)
            .mark_line(size=3)
            .encode(
                x=alt.X("Year",title='Year'),
                y=alt.Y("Suicides/100kPop",title='Suicide Rates',scale=alt.Scale(zero=False)),
                color='Gender',
                
                
                        
        ))
                

        points = lines.transform_filter(hover).mark_square(size=100)

        tooltips = (
            alt.Chart(data)
            .mark_rule(size=3,color='#628c43')
            .encode(
                x="Year",
                y="Suicides/100kPop",
                color='Gender',
                opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
                tooltip=[
                    alt.Tooltip("Year", title="year"),
                    alt.Tooltip("Gender", title="Gender"),
                    alt.Tooltip("Suicides/100kPop", title="Suicides/100kPop"),
                ],
            )
            .add_selection(hover)
        )
        return (lines+points+tooltips).interactive().properties(
        width=1000,
        height=600
    )

    chart2 = get_chart(source2)

    st.altair_chart(chart2, use_container_width=False)


    st.markdown('### Donut Chart')

    data4=data.groupby(['Gender']).sum()
    data4=data4.reset_index()
    data4=data4.drop(['Suicides/100kPop', 'GdpPerCapitalMoney',"Year"],axis=1)
    data4['Suicides/100kPop']=(data4['SuicidesNo']/data4['Population'])*100000
        
        
    plost.donut_chart(
    data=data4,
    theta="Suicides/100kPop",
    color='Gender',
    legend='bottom', 
    height=600,
    width=600,
    use_container_width=True)
    
with tab3:
    st.markdown('### Worldwide Suicide Rates')
    data2=data.groupby('Year').sum()
    data2=data2.drop(['Suicides/100kPop', 'GdpPerCapitalMoney'],axis=1)
    data2['Suicides/100kPop']=(data2['SuicidesNo']/data2['Population'])*100000
    data2=data2.reset_index()
    def get_chart(data):
            hover = alt.selection_single(
                fields=["Year"],
                nearest=True,
                on="mouseover",
                
            )
            
            lines = (
                alt.Chart(data)
                .mark_line(size=5,color='#328ba8')
                .encode(
                    x=alt.X("Year",title='Year'),
                    y=alt.Y("Suicides/100kPop",title='Suicide Rates',scale=alt.Scale(zero=False)),
                    
                            
            ))              

            points = lines.transform_filter(hover).mark_circle(size=300,color='#bd4d65')
                

            tooltips = (
                alt.Chart(data)
                .mark_rule(size=3,color='#bd4d65')
                .encode(
                    x="Year",
                    y="Suicides/100kPop",
                    
                    opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
                    tooltip=[
                        alt.Tooltip("Year", title="year"),
                        alt.Tooltip("Suicides/100kPop", title="Suicides/100kPop"),
                    ],
                )
                .add_selection(hover)
            )
            return (lines+points+tooltips).interactive().properties(
        width=1000,
        height=600
    )

    chart = get_chart(data2)

    st.altair_chart(chart, use_container_width=False)