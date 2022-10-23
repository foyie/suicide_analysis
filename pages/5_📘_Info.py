import streamlit as st
import time 
from streamlit_lottie import st_lottie
import json
import requests 

st.title("Information")

my_bar = st.progress(0)

for percent_complete in range(100):
    time.sleep(0.001)
    my_bar.progress(percent_complete + 1)



st.error('''Suicide is never an option. The world has become a better place in the last decade and mental
         health is more talked about.''', icon="🚨")

st.success('''Click this link to get the list of all the suicide helplines.''', icon="🚨")

st.subheader('''This analysis has been done on the kaggle suicide data set on WHO statistics ''')


st.markdown('''[`link`](https://www.kaggle.com/datasets/russellyates88/suicide-rates-overview-1985-to-2016)''')
def load_lottieurl(url: str):
                r = requests.get(url)
                if r.status_code != 200:
                    return None
                return r.json()
lottie_end = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_9ndsxmqq.json")
st_lottie(
                lottie_end,
                speed=1,
                reverse=False,
                loop=True,
                quality="low", # medium ; high
                #renderer=None, # canvas
                # height=400,
                # width=300,
                key=None,
            )




with st.sidebar:
    
    lottie_hello = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_SfcXWTUpiW.json")
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
    

