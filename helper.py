import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from urlextract import URLExtract
from collections import Counter
import emoji

ext = URLExtract()

def fetch_stats(selected_user,df):
  if selected_user !='Overall':
    df = df[df['user'] == selected_user]
  
  num_messages = df.shape[0]
  num_words = len((" ".join((df['message'].values.tolist()))).split())
  num_links = len(ext.find_urls(' '.join(df['message'].values.tolist())))
  media_list = ['<Media omitted>', '<\u200eimage omitted>','<\u200evideo omitted>','<\u200eGIF omitted>']
  num_media = (df[df['message'].str.strip().isin(media_list)]).shape[0]
  return num_messages,num_words,num_media,num_links

def most_busy_users(df):
  user_per = round((df['user'].value_counts().head() / df['user'].shape[0] )*100,2)
  user_per = user_per.reset_index().rename(columns={'user':'Person','count':'Percentage'})
  return user_per


def create_wordcloud(selected_user,df):
  if selected_user != 'Overall':
    df = df[df['user'] == selected_user]
  temp_df = df[df['user'] != 'group_notification']
  media_list = ['<Media omitted>', '<\u200eimage omitted>','<\u200evideo omitted>','<\u200eGIF omitted>']
  temp_df = temp_df[~temp_df['message'].str.strip().isin(media_list)]
  wc= WordCloud(width=500, height=500,min_font_size=10, background_color='white')
  wc_obj = wc.generate(' '.join(temp_df['message'].values.tolist()))
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
  most_common_df.rename(columns={0:'word',1:'frequency'}, inplace=True)
  return most_common_df


def emoji_helper(selected_user,df):
  if selected_user != 'Overall':
    df = df[df['user'] == selected_user]

  emojis = []
  for message in df['message']:
    all_emoji = emoji.emoji_list(message)
    for i in all_emoji:
      emojis.append(i['emoji'])
  emoji_df = pd.DataFrame(Counter(emojis).most_common(20))
  emoji_df.rename(columns={0:'emoji',1:'frequency'}, inplace=True)
  return emoji_df

def monthly_timeline(selected_user,df):
  if selected_user != 'Overall':
    df = df[df['user'] == selected_user]

  timeline = df.groupby(['year', 'month','month_num']).count()['message'].reset_index()
  timeline['time'] = timeline['month'] + '-' + timeline['year'].astype(str)
  return timeline

def daily_timeline(selected_user,df):
  if selected_user !='Overall':
    df = df[df['user'] == selected_user]

  timeline = df.groupby(['only_date']).count()['message'].reset_index()
  timeline['only_date'] = timeline['only_date'].astype(str)
  return timeline

def weekly_activity_map(selected_user,df):
  if selected_user !='Overall':
    df = df[df['user'] == selected_user]
  timeline = df.groupby(['day_name']).count()['message'].reset_index()
  return timeline

def monthly_activity_map(selected_user,df):
  if selected_user !='Overall':
    df = df[df['user'] == selected_user]
  timeline = df.groupby(['month']).count()['message'].reset_index()
  return timeline

def activity_heatmap(selected_user,df):
  if selected_user !='Overall':
    df = df[df['user'] == selected_user]
  
  pt = df.pivot_table(index='day_name',columns='period', values='message', aggfunc='count').fillna(0)

  return pt