
import pandas as pd
import altair as alt 
import streamlit as st
import time

my_bar = st.progress(0)

for percent_complete in range(100):
    time.sleep(0.001)
    my_bar.progress(percent_complete + 1)

tab1, tab2 = st.tabs(["Line Chart", "Bar plot"])
data=pd.read_csv('filt_data.csv')
mind=int(data['Year'].min())
maxd=int(data['Year'].max())


with st.sidebar:

    st.sidebar.header('`Pick Filters`⬇️')
    years = st.slider('Please select a range of year',mind,maxd , (1990, 2000))
    start=years[0]
    end=years[1]
    year_list=[]
    for i in range(start,end+1):
        year_list.append(i)

    countries = st.multiselect(
    'Select Country:',
    list(data['Country'].unique()),list(data['Country'].unique())[:4],
    )

    df_country=data[(data.Country.isin(countries))&(data.Year.isin(year_list))]
    df_country=df_country.drop([ 'Gender', 'Age', 'SuicidesNo', 'Population',
        'GdpForYearMoney', 'GdpPerCapitalMoney',
       'Generation'],axis=1)
    st.dataframe(df_country)
    st.sidebar.markdown('''
---
*Created with* ❤️ by [Foyie](https://github.com/foyie).
''')
    

with tab1:
    
    st.subheader('*Line Chart of the rate in different countries*')
    d=data[(data.Country.isin(countries))&(data.Year.isin(year_list))]
    d=d.groupby(['Country','Year']).sum()
    d=d.drop(['Suicides/100kPop',
        'GdpPerCapitalMoney'],axis=1)
    d['Suicides/100kPop']=(d['SuicidesNo']/d['Population'])*100000
    d=d.reset_index()
    source=d


    def get_chart(data):
        hover = alt.selection_single(
            fields=["Year"],
            nearest=True,
            on="mouseover",
            empty="none",
            
        )
        
        lines = (
            alt.Chart(data, title="Suicide Rates by Country ")
            .mark_line(size=3)
            .encode(
                x=alt.X("Year",title='Year'),
                y=alt.Y("Suicides/100kPop",title='Suicide Rates',scale=alt.Scale(zero=True)),
                # color='Country',
                color=alt.Color('Country',scale=alt.Scale(scheme='viridis')),
                
                
                        
        ))

        points = lines.transform_filter(hover).mark_square(size=100)

        tooltips = (
            alt.Chart(data)
            .mark_rule(size=2,color='#628c43')
            .encode(
                x="Year",
                y="Suicides/100kPop",
                color='Country',
                        
                
                opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
                tooltip=[
                    alt.Tooltip("Year", title="year"),
                    alt.Tooltip("Country", title="Country"),
                    alt.Tooltip("Suicides/100kPop", title="Suicides/100kPop"),
                ],
            )
            .add_selection(hover)
        )
        return (lines+points+tooltips).interactive().properties(
        width=1000,
        height=500
    )

    chart = get_chart(source)

    st.altair_chart(chart, use_container_width=False)
  
with tab2:
        
        st.subheader("*Bar plot for different countries*") 
        
        hover = alt.selection_single(fields=['Suicides/100kPop'],
                    nearest=True,
                    
                    on="mouseover",
                    )   
   
        
        for i in range(len(countries)):
            c=countries[i]
            df_c=source[source['Country']==c]
            st.subheader(c)    
            

            c_chart = (alt.Chart(df_c).mark_bar(size=10).encode(
            #alt.Column('Country'), 
            alt.X('Year',axis=alt.Axis(grid=False)),
            alt.Y('Suicides/100kPop',axis=alt.Axis(grid=True)), 
            alt.Color('Year',scale=alt.Scale(scheme='RedPurple')),
            opacity=alt.condition(hover, alt.value(1), alt.value(0.5)),  
                
            tooltip=[
                                    alt.Tooltip("Country", title="Country"),
                                    # alt.Tooltip("continent", title="continent"),
                                    alt.Tooltip("Suicides/100kPop", title="Suicides/100kPop"),
                                ]).interactive().add_selection(hover).properties(
            width=600,
            height=500
            )
                            )
            st.altair_chart(c_chart)                
            