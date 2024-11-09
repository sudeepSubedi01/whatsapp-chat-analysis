import streamlit as st
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
    num_messages,num_words,num_media,num_links = helper.fetch_stats(selected_user,df)
    
    col1,col2,col3,col4 = st.columns(4)
    with col1:
      st.title(num_messages)
      st.header('Total Messages')
    with col2:
      st.title(num_words)
      st.header('Total Words')
    with col3:
      st.title(num_media)
      st.header('Total Media')
    with col4:
      st.title(num_links)
      st.header('Total Links')


