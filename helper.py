import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from urlextract import URLExtract
from collections import Counter
import streamlit as st
ext = URLExtract()
def fetch_stats(selected_user,df):
  if selected_user =='Overall':
    num_messages = df.shape[0]                                                          # TOTAL MESSAGES
    num_words = len((" ".join((df['message'].values.tolist()))).split())                # TOTAL WORDS
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]                       # TOTAL MEDIA
    num_links = len(ext.find_urls(' '.join(df['message'].values.tolist())))             # TOTAL LINKS
  else:
    num_messages = df[df['user'] == selected_user].shape[0]                             # TOTAL MESSAGES
    new_df = df[df['user'] == selected_user]                                            # TOTAL WORDS
    num_words = len((' '.join(new_df['message'].values.tolist())).split())
    num_media = new_df[new_df['message'] == '<Media omitted>\n'].shape[0]               # TOTAL MEDIA
    num_links = len(ext.find_urls(' '.join(new_df['message'].values.tolist())))         # TOTAL LINKS

  
  return num_messages,num_words, num_media, num_links


def most_busy_users(df):
  user_per = round((df['user'].value_counts().head() / df['user'].shape[0] )*100,2)
  user_per = user_per.reset_index().rename(columns={'user':'Person','count':'Percentage'})
  return user_per


def create_wordcloud(selected_user,df):
  if selected_user != 'Overall':
    df = df[df['user'] == selected_user]
  wc= WordCloud(width=500, height=500,min_font_size=10, background_color='white')
  wc_obj = wc.generate(' '.join(df['message'].values.tolist()))
  return wc_obj


def most_common_words(selected_user,df):
  f = open('stop_hinglish.txt','r')
  stop_words = f.read()
  stop_words = stop_words.split()

  if selected_user != 'Overall':
    df = df[df['user'] == selected_user]

  temp_df = df[df['user'] != 'group_notification']
  media_list = ['<Media omitted>', '<\u200eimage omitted>','<\u200evideo omitted>','<\u200eGIF omitted>']
  temp_df = temp_df[~temp_df['message'].str.strip().isin(media_list)]
  words = []
  for message in temp_df['message']:
    for msg in message.lower().split():
      if msg not in stop_words:
        words.append(msg)
  most_common_df = pd.DataFrame(Counter(words).most_common(10))
  return most_common_df