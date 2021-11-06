import streamlit as st
import pandas as pd
import plotly.express as px
from statsmodels.tsa.arima.model import ARIMA
import datetime
import pickle
import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)
def pc_main():
    st.subheader('Daily positive cases count')
    final_data=pd.read_csv('/Users/tirumaleshn2000/Desktop/mini_project_final_files/final_confirmed_data.csv')
    #st.dataframe(data_frame.tail())
    final_data['Date_YMD']=pd.to_datetime(final_data['Date_YMD'])
    #st.dataframe(final_data)
    plt.title('Forecast of daily cases in India')
    plt.plot(final_data['Date_YMD'],final_data[['TT','final_tt_data_forecast']]);
    plt.xticks(rotation=90);
    plt.xlabel('Date');
    plt.ylabel('Count of cases');
    st.pyplot(plt.show())
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    recorded_data=go.Line(x=final_data['Date_YMD'][:571],y=final_data['TT'].dropna(),name='Recorded data')
    forecasted_data=go.Line(x=final_data['Date_YMD'][571:],y=final_data['final_tt_data_forecast'].dropna(),name='Forecasted data')
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(recorded_data)
    fig.add_trace(forecasted_data,secondary_y=True)
    st.subheader('Plot to interact')
    #fig.update_layout(xaxis=dict(tickangle=90))
    #fig=px.line(x=final_data['Date_YMD'],y=final_data['final_tt_data'],title='Interact with forecasted data here')
    st.write(fig)
    #st.dataframe(final_data)
