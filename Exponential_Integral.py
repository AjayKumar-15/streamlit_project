#Exponential Integeration
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import math
from PIL import Image

st.set_page_config(page_title="Data is OIL", layout="wide")

st.title("Power Series Expansion of Exponential Integral function")

image = Image.open('func.png')
st.image(image, caption="Series representation of Exponential Integral", width=None, use_column_width=None, clamp=False, channels='RGB', output_format='auto')

st.markdown("Making function E(X)")
n=st.number_input("No of Steps in Summation part of function:",value=1000)

#n=st.selectbox("No of Steps in Summation part of function :",[10,100,500,1000,2000])
n=int(n)
def E(X):
  ans=0
  for i in range(n):
    ans-=-1**(i+1)*X**(i+1)/(math.factorial(i+1)*(i+1))
    return ans


start=float(st.number_input("Starting value of x:",value=0.001,format="%.4f"))
end=int(st.number_input("End value of x:",value=2))
step=float(st.number_input("step value of x",value=0.001,format="%.4f"))

x=np.arange(start,end,step)
x=np.array(x)
#Log Approximation(x<0.01)
y1=-0.5772-np.log(x)
#Without Approximtion
y2=y1+E(x)


data=pd.DataFrame({"x":x,"E(x)":y2,"-0.5772-ln(x)":y1})
if st.checkbox("Show Raw Data",False):
    st.subheader("Raw Data")
    st.write(data)

st.subheader("Plot of function")
st.markdown("Comparision of E(x) and log_Approx")
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y1,
                    mode='lines',
                    name='log_Approx'))
fig.add_trace(go.Scatter(x=x, y=y2,
                    mode='lines',
                    name='E(X)'))
fig.update(layout_xaxis_range = [-0.1,end])

st.write(fig)
st.subheader("Conclusion")
st.markdown("we can see here,For lesser value of x both functions coincide to each other, so we can replace the E(x) function by approx_logarithmic function that is -0.5772-log(x) ")
st.write("Thank You")
st.write("Ajay")
