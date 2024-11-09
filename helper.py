from urlextract import URLExtract
ext = URLExtract()
def fetch_stats(selected_user,df):
  if selected_user =='Overall':
    num_messages = df.shape[0]                                                      # TOTAL MESSAGES
    num_words = len((" ".join((df['message'].values.tolist()))).split())            # TOTAL WORDS
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]
    num_links = len(ext.find_urls(' '.join(df['message'].values.tolist())))
  else:
    num_messages = df[df['user'] == selected_user].shape[0]                         # TOTAL MESSAGES
    new_df = df[df['user'] == df['user'][3]]                                        # TOTAL WORDS
    num_words = len((' '.join(new_df['message'].values.tolist())).split())
    num_media = new_df[new_df['message'] == '<Media omitted>\n'].shape[0]
    num_links = len(ext.find_urls(' '.join(new_df['message'].values.tolist())))

  
  return num_messages,num_words, num_media, num_links

  # TOTAL WORDS