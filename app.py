
import pandas as pd
from collections import Counter
import streamlit as st
import matplotlib.pyplot as plt
import preprocessor
import helper

st.sidebar.header('WhatApp Chat Analyser')
uploaded_file = st.sidebar.file_uploader('Choose a file:', type='txt')
# st.write(uploaded_file)
if uploaded_file is not None:
  bytes_data = uploaded_file.getvalue()
  data = bytes_data.decode('utf-8')
  # st.text(data)

  # DATA PREPROCESSING
  df = preprocessor.preprocess(data)
  st.dataframe(df)

  # SELECTBOX
  user_list = df['user'].unique().tolist()
  user_list.remove('group_notification')
  user_list.insert(0,'Overall')
  selected_user = st.sidebar.selectbox('Show analysis wrt', user_list)

  # BUTTON
  if st.sidebar.button('Show Analysis'):
    num_messages,num_words,num_media,num_links = helper.fetch_stats(selected_user,df)        # DISPLAYING STATS
    col1,col2,col3,col4 = st.columns(4)
    with col1:
      st.title(num_messages)
      st.header('Total Messages')
    with col2:
      st.title(num_words)
      st.header('Total Words')
    with col3:
      st.title(num_media)
      st.header('Media Shared')
    with col4:
      st.title(num_links)
      st.header('Links Shared')

    # MOST BUSY PERSONS
    if selected_user == 'Overall':
      st.title('Most Busy persons')
      col1,col2 = st.columns(2, gap='large')
      with col1:
        user_per = helper.most_busy_users(df)
        st.bar_chart(user_per,x='Person',y='Percentage', color='#ffaa00')
      with col2:
        st.dataframe(user_per)

    # WORD CLOUD
    st.title('Word Cloud')
    wc_obj = helper.create_wordcloud(selected_user,df)
    fig,ax=plt.subplots(figsize=(8,8))
    ax.axis('off')
    ax.imshow(wc_obj)
    st.pyplot(fig)

    # MOST COMMON WORDS
    st.title('Most Common Words')
    most_common_df = helper.most_common_words(selected_user,df)
    # st.dataframe(most_common_df)
    fig,ax = plt.subplots()
    ax.barh(most_common_df[0], most_common_df[1])
    st.pyplot(fig)
