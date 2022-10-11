#!/usr/bin/env python
# coding: utf-8

# In[13]:


import numpy as np
from pathlib import Path
import pandas as pd



FILE_NAME = "humandata_all.csv"

def handle_running_from_different_directories(file_name: str):
    cwd = Path.cwd()
    base =  "csv" / Path(file_name)
    if (cwd / base).exists():
        return cwd / base
    elif (cwd / ".." / base).exists():
        return cwd / ".." / base
    
csv_loc = handle_running_from_different_directories(FILE_NAME)
csv_loc = handle_running_from_different_directories(FILE_NAME)

df = pd.read_csv(csv_loc)

print(df.columns[1])
print(df.columns[2])
print(df.columns[1].split("_"))


    


# In[16]:


def find_algorithm_names(df):
    algorithm_names=[]
    for column_headers in df.columns:
        strsplit= column_headers.split("_")
        if len(strsplit)>1:
            if strsplit[1] not in algorithm_names:
                algorithm_names.append(strsplit[1])
    return algorithm_names

algorithm_names=find_algorithm_names(df)
print(algorithm_names)


# In[18]:


import streamlit as st
st.write ("""
#My first app
Hello world
""")


# In[ ]:




