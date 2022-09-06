import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import math
from PIL import Image

st.set_page_config(page_title="Well Testing", layout="wide")

st.title("Well Testing")
st.markdown("Upload Excel file consists of flowing pressure(pwf) and Time(t)")
file=st.file_uploader("Choose a file")

#@st.cache(persist=True)
if file is None:
    st.warning("You need to upload csv or Excel file")

else:
    data=pd.read_excel(file)

if st.checkbox("Show Raw Data",False):
    st.subheader("Raw Data")
    st.write(data)

column1=data.columns[0]
column2=data.columns[1]

st.header("Different plot types")
select=st.selectbox('Plot the graph by ', ['Normal','Semi-log','Log-log'])

x=data.iloc[:,0].values
y=data.iloc[:,1].values

#making straight line plot
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()


if select=="Normal":
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x,
        y=y
       ))
    st.write("Choose the interval value of x")
    start_x=float(st.number_input("Enter the starting value of x:"))
    end_x=float(st.number_input("Enter the end value of x:"))
    filtered=data[(data[column1]>=start_x)& (data[column1]<(end_x))]
    new_x=data.iloc[:,0].values
    new_y=data.iloc[:,1].values
    new_x=new_x.reshape(len(new_x),1)
    regressor.fit(new_x,new_y)
    pred_y=regressor.predict(new_x)
    fig.add_trace(go.Scatter(
        x=new_x,
        y=pred_y
       ))
    st.write(fig)
    fig.update_layout(title_text = "Pwf vs t")
    fig.update_xaxes(title_text="t")
    fig.update_yaxes(title_text="pwf")
    fig.show()
elif select=="Semi-log":
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x,
        y=y
       ))
    fig.update_layout(xaxis_type="log")
    fig.update_layout(title_text = "Semi- log plot of Pwf vs t")
    fig.update_xaxes(title_text="t")
    fig.update_yaxes(title_text="pwf")
    st.write(fig)
    fig.show()
else:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x,
        y=y
       ))
    fig.update_layout(xaxis_type="log",yaxis_type="log")
    fig.update_xaxes(title_text="t")
    fig.update_yaxes(title_text="pwf")
    fig.update_layout(title_text = "log-log plot of pwf vs t")
    st.write(fig)
    fig.show()
