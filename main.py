import streamlit as st
import numpy as np
import pandas as pd
from plotly import tools
import plotly.offline as py
import plotly.express as px
import boto3
import pickle
import urllib.request as urlrq
import certifi
from datetime import date
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#########
st.set_page_config(
    page_title="Covid 19 Forecast",
    page_icon="🦠📈",
    initial_sidebar_state="expanded",)
###########
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.title('Covid 19 Analysis and Forecast')
st.markdown('**Data:-** [Here](https://covid19.who.int/WHO-COVID-19-global-data.csv)')
st.markdown('*Note: The dataset is differed from the actual data read for training and tuning the model')
s3_resource = boto3.resource('s3',
        aws_access_key_id = '',
        aws_secret_access_key = '',
        region_name = 'us-east-1')
client = boto3.client(
        's3',
        aws_access_key_id = '',
        aws_secret_access_key = '',
        region_name = 'us-east-1'
    )
info_empty=st.empty()
info_empty.info('Loading the model. Please wait....')

@st.cache(suppress_st_warning=True,allow_output_mutation=True,show_spinner=False)
#reading the pickle file
def reading_files():
    india_model = pickle.loads(s3_resource.Bucket("deployments2021").Object('covid19_forecast/india_model.pkl').get()['Body'].read())
    #with open('/users/tirumaleshn2000/downloads/test_model.pkl','rb') as file:
    #    india_model=pickle.load(file)
    #reading dataframe
    info_empty.info('Loading the data')
    resp = urlrq.urlopen('https://covid19.who.int/WHO-COVID-19-global-data.csv', cafile=certifi.where())
    data_frame=pd.read_csv(resp)
    india_data=data_frame[data_frame['Country']=='India'].copy()
    india_data.reset_index(inplace=True)
    return [india_model,india_data]
read_file=reading_files()
india_model=read_file[0]
india_data=read_file[1]

info_empty.write('')
with st.form('covid'):
    number_of_days=st.slider('Number of days to forecast',min_value=1,max_value=400,key=1)

    if st.form_submit_button('Forecast'):
        future_dates=range(len(india_data),len(india_data)+number_of_days)
        future_data=pd.DataFrame(index=future_dates,columns=india_data.columns)
        final_data=pd.concat([india_data,future_data])
        today = date.today()
        final_data['final_tt_data_forecast']=india_model.predict(start=len(india_data),end=len(india_data)+number_of_days,dynamic=True)

        final_data['Date_reported'].iloc[india_data.index[-1]+1:]=pd.date_range(start=str(today),periods=number_of_days,freq='D')
        final_data['Date_reported']=pd.to_datetime(final_data['Date_reported'])
        plt.title('Forecast of daily cases in India')
        #fig = px.line(x=final_data['Date_reported'],y=final_data[['New_cases','final_tt_data_forecast']])

        recorded_data=go.Line(x=final_data[final_data['New_cases'].isnull()==False]['Date_reported'],y=final_data['New_cases'].dropna(),name='Recorded data')
        forecasted_data=go.Line(x=final_data[final_data['New_cases'].isnull()==True]['Date_reported'],y=final_data['final_tt_data_forecast'].dropna().astype(int),name='Forecasted data')
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(recorded_data)
        fig.add_trace(forecasted_data,secondary_y=True)
        st.subheader('Plot to interact')
        #fig.update_layout(xaxis=dict(tickangle=90))
        #fig=px.line(x=final_data['Date_YMD'],y=final_data['final_tt_data'],title='Interact with forecasted data here')
        st.write(fig)

st.subheader('This deployment is done as a part of our mini-project.')
st.markdown('Developed with streamlit and python')
st.markdown('Click this [link](https://github.com/tirumaleshn2000/Mini-project-files-B13-batch10/tree/deployment_files) for project files and other details')
