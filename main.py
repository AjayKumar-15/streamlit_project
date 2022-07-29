import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Data is OIL", page_icon=":bar_chart:", layout="wide")

#@st.cache
  #def get_data():
    #data = pd.read_csv('data/taxi_data.csv')
    #return data'''

siteHeader=st.container()
dataExploration=st.container()
newFeatures=st.container()
modelTraining=st.container()

st.text("Hello welcome to my app!")

with siteHeader:
    st.title('Welcome to the Awesome Project!')
    st.text('In this project I look into the dataset of volvo field to predict facies that is rock type')

with dataExploration:
    st.header("Dataset: Volve field dataset")
    st.text("It is open source data available on the internet")
    #Load data
    well_13 = pd.read_excel('VolveData_Project.xlsx', sheet_name='well 13',index_col=0)
    well_14 = pd.read_excel('VolveData_Project.xlsx', sheet_name='well 14')
    well_15 = pd.read_excel('VolveData_Project.xlsx', sheet_name='well 15')



    data = pd.concat([well_14, well_15],ignore_index=True, axis=0)
    data['Well'] = data['Well'].astype('category')
    data['RT_log'] = np.log10(data.RT) #For Visualization

    st.dataframe(data)

    # ---- SIDEBAR ----
    st.sidebar.header("Please Filter Here:")
    Facies = st.sidebar.multiselect(
    "Select the Facies:",
    options=data["Facies"].unique(),
    default=data["Facies"].unique()
    )


    df_selection = data.query(
    "Facies == @Facies")






with newFeatures:
    st.header('New features I came up with')
    st.text('Let\'s take a look into thre features generated.')

with modelTraining:

    max_depth = st.slider('What should be the max_depth of the model?',
    min_value=10, max_value=100,
    value=20,
    step=10)

    st.header('Model training')
    st.text('In this section you can select the hyperparamters!')
    st.text('Here is a list of features: ')
    st.write(data.columns)
    input_feature = st.text_input
    ('Which feature would you like to input to the model?',
    'PULocationID')

    number_of_trees = st.selectbox('How many trees should there be?',
    options=[100,200,300,'No limit'],
    index=0)
