#import packages

from datetime import datetime
from iexfinance.stocks import get_historical_data
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
from plotly.subplots import make_subplots

from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("iex_pub")
type(api_key)


#create date range

start = datetime(2019, 1, 1)
end = datetime.today()

#get ticker data

ticker_df = pd.read_csv('ticker_data.csv')
tickers = ticker_df.Symbol.values.tolist()

#create title for dashboard

st.title('Finance Portal')

#create sidebar with options

sidebar = st.sidebar.selectbox('Select an Option',['Stocks', 'Crypto','Fixed Income'])

 

#Activate your dashboard
#streamlit run dashboard.py

if sidebar == 'Stocks':
    exchange = st.radio('select an exchange or Ticker', ['S&P 500', 'Nasdaq', 'Search by Ticker'])
    if exchange == 'S&P 500':
        dropdown = st.selectbox('Select a Ticker', tickers)
        df = get_historical_data(
                                 dropdown, 
                                 start, 
                                 end,
                                 output_format='pandas', 
                                 token=api_key)
        fig = px.line(df, x=df.index, y=df.close, title=str(dropdown)+' 2019 Performance')



first_value = df.close.iloc[0]
last_value = df.close.iloc[-1]
change = (last_value - first_value)/first_value
if change > 0:
   st.write("This stock was up {:.2f}".format(change)+ '%')
elif change < 0:
   st.write("This stock was down {:.2f}".format(change)+ '%')



#create subheader
st.subheader('Did Your Stock Beat the market?')

#get S&P 500 data
df2 = yf.download('%5EGSPC', start=start, end=end


#first observation
sp_perf_1 = df2.Close.iloc[0]

#last observation
sp_perf_last = df2.Close.iloc[-1]

#calculate % change      
sp_perf = (sp_perf_last-sp_perf_1)/sp_perf_1

#graph data
perf_graph = make_subplots(specs=[[{"secondary_y": True}]])
perf_graph.add_trace(go.Scatter(x=df2.index, y=df2.Close, mode='lines', name='S&P 500'),secondary_y=False)
perf_graph.add_trace(go.Scatter(x=df.index, y=df.close, mode='lines', name=dropdown),secondary_y=True)
        
#display graph
st.plotly_chart(perf_graph)

#display percentage change
st.write("S&P's Performance: {:.2f} ".format(sp_perf))
st.write(dropdown + "'s performance: {:.2f} ".format(change))