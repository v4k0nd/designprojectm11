#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def find_algorithm_names(df):
    algorithm_names=[]
    for column_headers in df.columns:
        strsplit= column_headers.split("_")
        if len(strsplit)>1:
            if strsplit[1] not in algorithm_names:
                algorithm_names.append(strsplit[1])
    return algorithm_names

# algorithm_names=find_algorithm_names(df)
# print(algorithm_names)


# In[ ]:


from rich import print
from rich.console import Console
from rich.table import Table
from rich import box 
from sklearn import metrics
import streamlit as st

def table_setup():
#     table = Table(title="", box=box.ROUNDED)
#     table.add_column("")
#     table.add_column("predicted 0")
#     table.add_column("predicted 1")
#     return table
# console = Console(record=True)
    d = {' ': ["actual 0", "actual 1"], 'predicted 0': ["0","0"] , 'predicted 1' : ["0","0"]}
    dff = pd.DataFrame(data=d)
    return dff
def confusion_matrix_create (column_name,columnlabel):
    y = df["groundTruth"] # definite truth
    val_count = y.value_counts()
    total = len(y)
#     console.rule(f"[bold red]Confusion matrix ", align="left")
#     print(f"Nr of occurance of:\n{val_count}")
#     print(f"total {total}")
    dff = table_setup()
    X = df[column_name]
    # continue
    tn, fp, fn, tp = metrics.confusion_matrix(y, X).ravel()

    f1 = metrics.f1_score(y, X)

    #print
#     table.add_row("actual 0", "[blue]"+str(tn), str(fp))
#     table.add_row("actual 1", str(fn), "[blue]"+str(tp))
    dff['predicted 0']=[str(tn),str(fn)]
    dff['predicted 1']= [str(fp),str(tp)]
    
#     console.print(f"f1: [orange1]{f1}[/orange1]\n")
    blankIndex=[''] * len(dff)
    dff.index=blankIndex
    columnlabel.table(dff)
    new_title1 = '<p style="font-family:sans-serif; color:Black; font-size: 36px;">'
    format_float_f1 = "{:.2f}".format(f1)
    new_title2= 'F1 score: ' + str(format_float_f1)+'</p>'
    new_title=new_title1+new_title2
    columnlabel.markdown(new_title, unsafe_allow_html=True)
    print(dff)

    


# In[ ]:


import matplotlib.pyplot as plt
from sklearn.metrics import RocCurveDisplay

def ROC_create (column_name,columnlabel):
    y = df["groundTruth"] # definite truth
    val_count = y.value_counts()
    total = len(y)
    
    X = df[column_name]
    
    fig_roc=RocCurveDisplay.from_predictions(y, X)
#     plt.show()
    columnlabel.pyplot(fig_roc.figure_)


# In[ ]:


def show_results(algorithm_name,columnlabel):
    new_title1 = '<p style="font-family:sans-serif; color:Blue; font-size: 36px;">'
    new_title2= algorithm_name.capitalize()+' results</p>'
    new_title=new_title1+new_title2
    new_subtitle1= '<p style="font-family:sans-serif; color:Black; font-size: 12px; text-align: center;">'
    new_subtitle2= "ROC curve " + '</p'
    new_subtitle3= "Confusion matrix "+ '</p'
    columnlabel.markdown(new_title, unsafe_allow_html=True)
#     st.write (algorithm_name+ " algorithm results")
    columnlabel.markdown(new_subtitle1+new_subtitle2, unsafe_allow_html=True)
    ROC_create("accuracy_"+algorithm_name,columnlabel)
    columnlabel.markdown(new_subtitle1+new_subtitle3, unsafe_allow_html=True)
    confusion_matrix_create("labels_"+algorithm_name,columnlabel)
    


# In[ ]:





# In[ ]:





# In[44]:




    


# In[ ]:


import numpy as np
from pathlib import Path
import pandas as pd
import streamlit as st
uploaded_file = st.file_uploader("Choose a  CSV file",type=['csv'])

if uploaded_file is not None:
#read csv
    df=pd.read_csv(uploaded_file)
    temp_test=['detectron','detectron','detectron']
    columns= st.columns(len(temp_test),gap="medium")
    for i in range(0, len(temp_test)):
        show_results(temp_test[i],columns[i])


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




