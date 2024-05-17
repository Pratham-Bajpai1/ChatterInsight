from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import string
import emoji

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]


    # total messages
    total_messages = df.shape[0]

    # total words
    total_words = []
    for message in df['message']:
        total_words.extend(message.split())

    # total media files messages
    total_media_files = 0
    for media in df['message']:
        if media == '<Media omitted>\n':
            total_media_files = total_media_files + 1

    # total links in chat
    extractor = URLExtract() # object of URLExtract class
    total_links = []
    for message in df['message']:
        total_links.extend(extractor.find_urls(message))


    return total_messages, len(total_words), total_media_files, len(total_links)


def find_busy_persons(df):
    x = df['user'].value_counts().head()
    # find percentage of each users sending messages
    df = round((df['user'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns={'user':'name', 'count':'percent'})
    return x, df

def chat_wordCloud(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    #we can also removed stop words, media omitted etc.
    wordCloud = WordCloud(width=800, height=600, min_font_size=10, background_color='black') #generate an image
    df_wordCloud = wordCloud.generate(df['message'].str.cat(sep=" ")) # put all mostly used words in image.

    return df_wordCloud # return an wordcloud image

def common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # remove group messages (group notification)
    temp = df[df['user'] != 'group_notification']
    # remove media omitted message
    temp = temp[temp['message'] != '<Media omitted>\n']
    # remove all stop words
    words = []

    for message in temp['message']:
        for word in message.lower().split():  # convert in lower case
            # remove punctuation from each word
            word = word.translate(str.maketrans('', '', string.punctuation))
            if word not in stop_words: # remove stop words
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(25)).rename(columns={0:'words', 1:'frequency'})  # select most common 25 words from chat and convert into data frame then return data frame.

def emoji_analysis(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        list = emoji.analyze(message)
        for emo in list:
            emojis.append(emo.chars)

    emoji_df = pd.DataFrame(Counter(emojis).most_common()).rename(columns={0:'emojis', 1:'frequency'})

    return emoji_df

def timeline_analysis(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + " " + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


    """"
    if selected_user == 'Overall':
        # total messages
        total_messages = df.shape[0]

        # total words
        words = []
        for message in df['message']:
            words.extend(message.split())

        return total_messages, len(words)

    else:
        newdf = df[df['user'] == selected_user]
        total_messages = newdf.shape[0]

        words = []
        for message in newdf['message']:
            words.extend(message.split())

        return total_messages, len(words)
    """