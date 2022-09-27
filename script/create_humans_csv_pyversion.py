#!/usr/bin/env python
# coding: utf-8

# ## INSTRUCTIONS
# Put the contents of the archive from Julian in a folder called 'arisedataset'. Put the 'arisedataset' folder in the same
# directory as this pyscript.

# In[13]:


import pandas as pd

df = pd.read_csv('arisedataset/humandata.csv')
print(df['mediaID'])


# In[35]:



import shutil
import os

src_dir = "arisedataset/images"
dst_dir = "arisedataset/humanLabeledImages"
shutil.rmtree('arisedataset/humanLabeledImages')
if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)
for file in os.listdir(src_dir):
    if file.endswith(".jpg"):
        mediaID=file[0:len(file)-4]
        # since a photo can contain 2 species so mediaID is not unique
        listt=df.index[df["mediaID"]==mediaID].tolist()
        for x in listt:
            if df.iloc[[x]]["scientificName"].values[0]=="Homo sapiens":
                shutil.copy(src_dir+"/"+file,dst_dir+"/"+file)
                print("copied")
#         for i in range (len(df)):
#             if df.loc[i,"mediaID"]==mediaID:
#                 if df.loc[i,"scientificName"]=="Homo Sapiens":
#                     shutil.copy(src_dir+"/"+file,dst_dir+"/"+file)
#                     print("copied")
            
#        shutil.copy(src_dir+"/"+file,dst_dir+"/"+file)
#        print("copied")


# *** Now remove the non-human pictures and add them to humanLabeledImagesAndFIltered folder.

# In[40]:


import shutil
import os
df['human'] = pd.Series(dtype='int')
df['human'] = 0
src_dir = "arisedataset/humanLabeledImagesAndFIltered"
for file in os.listdir(src_dir):
    if file.endswith(".jpg"):
        mediaID=file[0:len(file)-4]  # cut the .jpg
        listt=df.index[df["mediaID"]==mediaID].tolist()
        for x in listt:
            df.at[x,'human']=1
pd.set_option('display.max_rows', None)
print(df['human'])


# In[42]:


df.to_csv("new_csv.csv")

