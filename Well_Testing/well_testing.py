import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
from sklearn.metrics import r2_score



if select=="Normal":
    fig = make_subplots()

    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        name="pwf vs t"
       ))
    st.write(fig)
    st.write("Choose the interval value of x")
    start_x=float(st.number_input("Enter the starting value of x:",value=0.000,format="%.3f"))
    end_x=float(st.number_input("Enter the end value of x:",value=10.00,format="%.2f"))
    filtered=data[(data[column1]>=start_x)& (data[column1]<(end_x))]
    new_x=filtered.iloc[:,0].values
    new_y=filtered.iloc[:,1].values
    new_x=new_x.reshape(len(new_x),1)
    regressor.fit(new_x,new_y)
    pred_y=regressor.predict(new_x)
    filtered["pred_pwf"]=pred_y
    if st.checkbox("Selected Data",False):
        st.subheader("Selected Data")
        st.write(filtered)

    fig.add_trace(go.Scatter(
        x=filtered[column1],
        y=filtered["pred_pwf"],
        name="trend line"
       ))

    fig.update_layout(title_text = "Pwf vs t")
    fig.update_xaxes(title_text="t")
    fig.update_yaxes(title_text="pwf")
    st.write(fig)
    slope=regressor.coef_[0]
    intercept=regressor.intercept_
    r2_score=r2_score(new_y, pred_y)
    st.write("#Info about Trendline")
    st.write("slope=",slope)
    st.write("Intercept=",intercept)
    st.write("r2_score=",r2_score)

elif select=="Semi-log":
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        name="pwf vs log(t)"
       ))
    fig.update_layout(xaxis_type="log")
    fig.update_xaxes(minor=dict(ticks="inside", ticklen=6, showgrid=True))
    fig.update_layout(title_text = "Semi- log plot of Pwf vs t")
    fig.update_xaxes(title_text="t")
    fig.update_yaxes(title_text="pwf")
    st.write(fig)
    st.write("Choose the interval value of x")
    start_x=float(st.number_input("Enter the starting value of x:",value=0.001,format="%.3f"))
    end_x=float(st.number_input("Enter the end value of x:",value=10.00,format="%.2f"))
    filtered=data[(data[column1]>=start_x)& (data[column1]<(end_x))]
    new_x=filtered.iloc[:,0].values
    new_y=filtered.iloc[:,1].values
    if st.checkbox("Selected Data",False):
        st.subheader("Selected Data")
        st.write(filtered)
    p = np.polyfit(np.log(new_x),new_y, 1)
    new_x=(new_x)
    pred_y=p[0]*np.log(new_x)+p[1]
    fig.add_trace(go.Scatter(
        x=new_x,
        y=pred_y,
        name="Trendline"
       ))
    fig.update_layout(xaxis_type="log")
    fig.update_layout(title_text = "Semi- log plot of Pwf vs t")
    fig.update_xaxes(title_text="t")
    fig.update_yaxes(title_text="pwf")
    fig.update_xaxes(minor=dict(ticks="inside", ticklen=6, showgrid=True))
    st.write(fig)

    r2_score=r2_score(new_y, pred_y)
    st.write("#Info about Trendline")
    st.write("slope=",p[0])
    st.write("Intercept=",p[1])
    st.write("r2_score=",r2_score)

    st.markdown("Calculation of Permeability and Skin")
    pi=st.number_input("Initial Pressure (psia):",value=3510.00)
    phi=st.number_input("Porosity:",value=0.18)
    swi=st.number_input("Initial water Saturation:",value=0.211)
    T=st.number_input("Temperature(K):",value=200.00)
    rw=st.number_input("radius of well (ft):",value=0.330)
    u=st.number_input("viscosity (cp):",value=1.000)
    Q=st.number_input("Flow rate(bbl/d):",value=1500.00)
    yo=st.number_input("specific_gravity:",value=0.70)
    C=st.number_input("Compressibilty(1/psi):",value=0.000015)
    Bo=st.number_input("Formation Volume Factor(rb/dtb):",value=1.20)
    A=st.number_input("Area(acre):",value=640.00)
    h=st.number_input("height of payzone (ft):", value=20.00)

    st.markdown(
        f"""
        * Pi(psia) : {pi}
        * phi : {phi}
        * swi : {swi}
        * T(K) : {T}
        * rw(ft) : {rw}
        * u(cp) : {u}
        * Q(bbl/d) : {Q}
        * Yo : {yo}
        * C(1/psi) : {C}
        * Bo(rb/stb): {Bo}
        * A(Acres) : {A}
        * h(ft) : {h}
        """)

    k=162.6*Q*Bo/(-1*p[0]*h)
    st.write(f"Permeabilty of well (md) is : ",k)
    pwf_1hr=p[1]
    s=1.151*((pi-pwf_1hr)/(-1*p[0])-np.log(k/(phi*u*C*rw*rw))+3.23)
    st.write("Skin of the well is ",s)








else:
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        name="log(p) vs log(t)"
       ))
    fig.update_layout(xaxis_type="log",yaxis_type="log")
    st.write(fig)
    st.write("Choose the interval value of x")
    start_x=float(st.number_input("Enter the starting value of x:",value=0.001,format="%.3f"))
    end_x=float(st.number_input("Enter the end value of x:",value=10.00,format="%.2f"))
    filtered=data[(data[column1]>=start_x)& (data[column1]<(end_x))]
    new_x=filtered.iloc[:,0].values
    new_y=filtered.iloc[:,1].values
    if st.checkbox("Selected Data",False):
        st.subheader("Selected Data")
        st.write(filtered)
    p = np.polyfit(np.log(new_x),np.log(new_y), 1)
    pred_y=np.exp(p[0]*np.log(new_x)+p[1])
    fig.add_trace(go.Scatter(
        x=new_x,
        y=pred_y,
        name="Trendline"
       ))

    fig.update_layout(xaxis_type="log",yaxis_type="log")
    fig.update_xaxes(title_text="t")
    fig.update_yaxes(title_text="pwf")
    fig.update_layout(title_text = "log-log plot of pwf vs t")
    st.write(fig)
    r2_score=r2_score(new_y, pred_y)
    st.write("#Info about Trendline")
    st.write("slope=",p[0])
    st.write("Intercept=",p[1])
    st.write("r2_score=",r2_score)

st.header("Diagnostic Plot")
pi=data[column2].values[0]

data["delta_p"]=pi-data[column2]
data["dt"]=data[column1].diff()
data["dp"]=abs(data[column2].diff())
data["p_dash"]=data["dp"]/data["dt"]*data[column1]
st.write(data)

fig = make_subplots()

fig.add_trace(go.Scatter(
    x=x,
    y=data["p_dash"],
    name="log(delta_p) vs log(t)"
   ))
"""fig.add_trace(go.Scatter(
    x=x,
    y=data[""],
    name="log(p_dash) vs log(t)"
   ))"""
fig.update_layout(xaxis_type="log",yaxis_type="log")
st.write(fig)
st.write("Choose the interval value of x")
sta_x=float(st.number_input("Enter the starting value of x:",value=0.001,format="%.3f"))
e_x=float(st.number_input("Enter the end value of x:",value=10.00,format="%.2f"))
filtered=data[(data[column1]>=sta_x)& (data[column1]<(e_x))]
new_x=filtered.iloc[:,0].values
new_y=filtered.iloc[:,["p_dash"]].values
if st.checkbox("Selected Data",False):
    st.subheader("Selected Data")
    st.write(filtered)
p = np.polyfit(np.log(new_x),np.log(new_y), 1)
pred_y=np.exp(p[0]*np.log(new_x)+p[1])
fig.add_trace(go.Scatter(
    x=new_x,
    y=pred_y,
    name="Trendline"
   ))

fig.update_layout(xaxis_type="log",yaxis_type="log")
fig.update_xaxes(title_text="t")
fig.update_yaxes(title_text="pwf")
fig.update_layout(title_text = "log-log plot of pwf vs t")
st.write(fig)
r2_score=r2_score(new_y, pred_y)
st.write("#Info about Trendline")
st.write("slope=",p[0])
st.write("Intercept=",p[1])
st.write("r2_score=",r2_score)
st.write(data)
