from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
extract=URLExtract()

def fetch_stats(selected_user,df):

    if selected_user !='Overall':
        df=df[df['user']==selected_user]
        
    num_messages=df.shape[0]
    #fetching words
    words=[]
    for message in df['message']:
        words.extend(message.split())

    #fetching images
    num_message_media=df[df['message']==''].shape[0]

    #fetching urls
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_message_media,len(links)

def most_busy_users(df):
    x=df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={"index":"name","user":"percent"})
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color="white")
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common_word(selected_user,df):
    # temp=df[df['message'] != '']
    f=open('D:\zeel\projects\whatsapp-chat-analysis\stop_hinglish.txt','r')
    stop_words=f.read()
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    
    
    words=[]
    for message in df['message']:
        for word in message.lower().split():
            if word not in stop_words:   
                words.append(word)
    most_common_word=pd.DataFrame(Counter(words).most_common(20))
    return most_common_word

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline["year"][i]))
    timeline['time']=time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    daily_timeline=df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    return df['day_name'].value_counts()

def monthly_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    return df['month'].value_counts()    