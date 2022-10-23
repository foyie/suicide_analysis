import streamlit as st
import pandas as pd
import altair as alt 
import plotly.express as px
from streamlit_lottie import st_lottie
import json
import requests 
import time 

st.title('🌏Suicide rate over Countries')

with st.spinner('Wait for it...'):
    time.sleep(3)
    

data=pd.read_csv('filt_data.csv')
data_count=data.groupby(['Country']).sum()
data_count=data_count.reset_index()
data_count=data_count.drop(['Suicides/100kPop', 'GdpPerCapitalMoney','Year'],axis=1)
data_count['Suicides/100kPop']=(data_count['SuicidesNo']/data_count['Population'])*100000



with st.sidebar:
        st.sidebar.header('`Suicide over countries`')
        
        st.subheader("These charts show the suicide rates over countries with respect to age,gender and generations ") 
        
        def load_lottieurl(url: str):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()

        lottie_hello = load_lottieurl("https://assets7.lottiefiles.com/private_files/lf30_of3skn6w.json")
        st_lottie(
            lottie_hello,
            speed=1,
            reverse=False,
            loop=True,
            quality="low", # medium ; high
            #renderer=None, # canvas
            height=400,
            width=350,
            key=None,
        )

        st.sidebar.markdown('''
---
*Created with* ❤️ by [Foyie](https://github.com/foyie).

''')



tab1, tab2,tab3,tab4 = st.tabs(["Country","By Gender",'By Age','Map'])

with tab1:
    
    st.header("Barchart for countries")


    hover = alt.selection_single(fields=['Suicides/100kPop'],
                    nearest=True,
                    
                    on="mouseover",
                    )
    gp_chart = (alt.Chart(data_count).mark_bar().encode(
    #alt.Column('continent'), 
    alt.X('Suicides/100kPop',axis=alt.Axis(labelAngle=0,tickCount=10)),
    alt.Y('Country',axis=alt.Axis(grid=False),sort='-x'), 
    alt.Color('Suicides/100kPop',scale=alt.Scale(scheme='purplered')),
    opacity=alt.condition(hover, alt.value(1), alt.value(0.8)),  
    tooltip=[
                            alt.Tooltip("Country", title="Country"),
                            
                            alt.Tooltip("Suicides/100kPop", title="Suicides/100kPop"),
                        ]
    ).interactive()
                .properties(
        width=1000,
        height=2000
    ).add_selection(hover)

        
    )

    st.altair_chart(gp_chart)

with tab2:
    st.info(' Stacked bar chart for suicide rates with respect to gender')
    data_count_g=data.groupby(['Country','Gender']).sum()
    data_count_g=data_count_g.reset_index()
    data_count_g=data_count_g.drop(['Suicides/100kPop', 'GdpPerCapitalMoney','Year'],axis=1)
    data_count_g['Suicides/100kPop']=(data_count_g['SuicidesNo']/data_count_g['Population'])*100000
    
    hover2 = alt.selection_single(fields=['Suicides/100kPop'],
                    nearest=True,
                    
                    on="mouseover",
                    )


    gend_chart = (alt.Chart(data_count_g).mark_bar().encode(
    #alt.Column('continent'), 
    alt.X('Suicides/100kPop',
            #axis=alt.Axis(labelAngle=0,tickCount=10)
            ),
    alt.Y('Country',axis=alt.Axis(grid=False),sort='-x'), 
    alt.Color('Gender',scale=alt.Scale(scheme='darkblue')),
    opacity=alt.condition(hover2, alt.value(1), alt.value(0.5)),  
    tooltip=[
                            alt.Tooltip("Country", title="Country"),
                            alt.Tooltip("Gender", title="Gender"),
                            alt.Tooltip("Suicides/100kPop", title="Suicides/100kPop"),
                        ]
    )
                .interactive()
                .properties(
        width=1000,
        height=2000
    ).add_selection(hover2)
                )
    st.altair_chart(gend_chart)
    
with tab3:
    st.warning(' Stacked bar chart for suicide rates with respect to age')
    data_count_a=data.groupby(['Country','Age']).sum()
    data_count_a=data_count_a.reset_index()
    data_count_a=data_count_a.drop(['Suicides/100kPop', 'GdpPerCapitalMoney','Year'],axis=1)
    data_count_a['Suicides/100kPop']=(data_count_a['SuicidesNo']/data_count_a['Population'])*100000
        
    hover3 = alt.selection_single(fields=['Suicides/100kPop'],
                    nearest=True,
                    
                    on="mouseover",
                    )


    gend_chart = (alt.Chart(data_count_a).mark_bar().encode(
    #alt.Column('continent'), 
    alt.X('Suicides/100kPop',
            #axis=alt.Axis(labelAngle=0,tickCount=10)
            ),
    alt.Y('Country',axis=alt.Axis(grid=False),sort='-x'), 
    alt.Color('Age',scale=alt.Scale(scheme='plasma')),
    opacity=alt.condition(hover3, alt.value(1), alt.value(0.7)),  
    tooltip=[
                            alt.Tooltip("Country", title="Country"),
                            alt.Tooltip("Age", title="Age"),
                            alt.Tooltip("Suicides/100kPop", title="Suicides/100kPop"),
                        ]
    )
                .interactive()
                .properties(
        width=1000,
        height=2000
    ).add_selection(hover3)
                )
    st.altair_chart(gend_chart)
    
with tab4:
    st.info(' Rates over countries on Worldmap')
    merge_conti=pd.read_csv('countries.csv')
    f_conti=px.choropleth(merge_conti,
                locationmode='country names',
                locations=merge_conti['Country'],
                # scope='world',
                color_continuous_scale="Plasma",
                height=600,
                width=1200,
                basemap_visible=True,
                # range_color=[8,20],
                
                #title='S',
                # projection='orthographic',
                hover_name=merge_conti['Country'],
                hover_data=['Suicides/100kPop'],
                color=merge_conti['Suicides/100kPop'])
    f_conti.update_layout(margin={"r":0,"t":0,"l":0,"b":0},hoverlabel=dict(bgcolor=px.colors.sequential.Plasma[5]))
    f_conti.update_geos(showcountries=True, showcoastlines=True, showland=False, fitbounds="locations",
               )
    st.plotly_chart(f_conti,use_container_width=False)
 
        

    







    
    
    