import streamlit as st
import preprocessing
import helperClass
import matplotlib.pyplot as plt
import numpy as np

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
    }
    .main {
        background: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
    }
    .sidebar .sidebar-content {
        background: #f5f5f5;
        padding: 10px;
        border-radius: 10px;
    }
    .title {
        color: #333333;
        text-align: center;
        font-family: 'Arial Black', Gadget, sans-serif;
        margin-bottom: 20px;
    }
    .header {
        color: #ff6347;
        text-align: center;
        font-family: 'Arial', sans-serif;
        margin-bottom: 10px;
    }
    .section-title {
        color: #333333;
        text-align: center;
        font-family: 'Arial Black', Gadget, sans-serif;
        margin-top: 30px;
        margin-bottom: 10px;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        font-family: 'Arial', sans-serif;
        color: #666666;
    }
    .dataframe {
        margin-top: 20px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar with title and file uploader
st.sidebar.title("WhatsApp Chat Analyzer")

# Adding a GIF to the sidebar
st.sidebar.markdown(
"""
    <div style="text-align: center;">
        <img src="https://i.gifer.com/75ez.gif" width="500" height="250">
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes
    bytes_data = uploaded_file.getvalue()
    # Convert bytes to string
    data = bytes_data.decode("utf-8")

    df = preprocessing.preprocess(data)  # Preprocess the chat data
    st.dataframe(df)  # Display the dataframe

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis with respect to", user_list)

    if st.sidebar.button("Show Analysis"):
        # Display stats
        st.markdown('<h1 class="title">Top Statistics</h1>', unsafe_allow_html=True)
        total_messages, total_words, total_media_files, total_links = helperClass.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown('<h2 class="header">Total Messages</h2>', unsafe_allow_html=True)
            st.title(total_messages)
        with col2:
            st.markdown('<h2 class="header">Total Words</h2>', unsafe_allow_html=True)
            st.title(total_words)
        with col3:
            st.markdown('<h2 class="header">Total Media Files</h2>', unsafe_allow_html=True)
            st.title(total_media_files)
        with col4:
            st.markdown('<h2 class="header">Total Links</h2>', unsafe_allow_html=True)
            st.title(total_links)

        # Display busy users for group level
        if selected_user == 'Overall':
            st.markdown('<h2 class="section-title">Busy Users</h2>', unsafe_allow_html=True)
            x, newdf = helperClass.find_busy_persons(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color="green")
                plt.xticks(rotation='vertical')
                plt.ylabel("No of Messages")
                plt.xlabel("Users")
                st.pyplot(fig)
            with col2:
                st.dataframe(newdf)

        # Display WordCloud
        st.markdown('<h2 class="section-title">WordCloud of Most Commonly Used Words</h2>', unsafe_allow_html=True)
        df_wordCloud = helperClass.chat_wordCloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wordCloud)
        st.pyplot(fig)

        # Display most common words
        st.markdown('<h2 class="section-title">Most 25 Common Words Used By User</h2>', unsafe_allow_html=True)
        common_words = helperClass.common_words(selected_user, df)
        st.dataframe(common_words)
        fig, ax = plt.subplots()
        ax.barh(common_words['words'], common_words['frequency'], color='#FFA07A')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Display emoji analysis
        st.markdown('<h2 class="section-title">Most Emojis Used</h2>', unsafe_allow_html=True)
        emoji_df = helperClass.emoji_analysis(selected_user, df)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['frequency'].head(), labels=emoji_df['emojis'].head(), autopct="%1.1f%%", colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
            st.pyplot(fig)
        with col3:
            fig, ax = plt.subplots()
            ax.bar(emoji_df['emojis'].head(), emoji_df['frequency'].head(), color='#FF4500')
            plt.ylabel("No. of Times Emoji Used")
            plt.xlabel("Emojis")
            st.pyplot(fig)

        # Display timeline analysis
        st.markdown('<h2 class="section-title">Monthly Timeline</h2>', unsafe_allow_html=True)
        timeline = helperClass.timeline_analysis(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

# Footer with copyright
st.markdown('<p class="footer">© 2024 Made By Pratham Bajpai</p>', unsafe_allow_html=True)




















# original previous code -
# import streamlit as st
# import preprocessing
# import helperClass
# import matplotlib.pyplot as plt
# import numpy as np
#
# st.sidebar.title("WhatsApp Chat Analyzer")
#
# uploaded_file = st.sidebar.file_uploader("Choose a file")
# if uploaded_file is not None:
#     # To read file as bytes
#     bytes_data = uploaded_file.getvalue()
#     #when we upload chat on web then chat in stream form (bytes form), we need to convert this chat into string.
#     data = bytes_data.decode("utf-8")
#
#     #st.text(data) #display chat on web
#
#     df = preprocessing.preprocess(data) #we pass given user chat data in preprocess function (preprocessing file) then this function return dataframe.
#     st.dataframe(df) #displaying dataframe in web
#
#     #fetch unique users
#     user_list = df['user'].unique().tolist()
#     user_list.remove('group_notification')
#     user_list.sort()
#     user_list.insert(0, "Overall")
#
#     selected_user = st.sidebar.selectbox("Show Analysis with respect to", user_list)
#
#     if st.sidebar.button("Show Analysis"):
#
#         # display stats
#         st.title("Top Statistics")
#         total_messages, total_words, total_media_files, total_links = helperClass.fetch_stats(selected_user, df)
#
#         col1, col2, col3, col4 = st.columns(4)
#
#         with col1:
#             st.header("Total Messages")
#             st.title(total_messages)
#
#         with col2:
#             st.header("Total Words")
#             st.title(total_words)
#
#         with col3:
#             st.header("Total Media Files")
#             st.title(total_media_files)
#
#         with col4:
#             st.header("Total Links")
#             st.title(total_links)
#
#         # finding busy users in the chat for Group Level
#         if selected_user == 'Overall':
#             st.title('Busy Users')
#             x, newdf = helperClass.find_busy_persons(df)
#             fig, ax = plt.subplots()
#             col1, col2 = st.columns(2)
#
#             with col1:
#                 ax.bar(x.index, x.values, color="green")
#                 plt.xticks(rotation='vertical')
#                 plt.ylabel("No of Messages")
#                 plt.xlabel("Users")
#                 st.pyplot(fig)
#
#             with col2:
#                 st.dataframe(newdf)
#
#         # Chat WordCloud
#         st.title("WorldCloud of Most Commonly Used Words")
#         df_wordCloud = helperClass.chat_wordCloud(selected_user, df) # wordcloud image
#         fig, ax = plt.subplots()
#         ax.imshow(df_wordCloud)
#         st.pyplot(fig)
#
#         # most common words used in chat
#         st.title("Most 25 Common Words Used By User")
#         common_words = helperClass.common_words(selected_user, df)
#         st.dataframe(common_words)
#
#         fig, ax = plt.subplots()
#         ax.barh(common_words['words'], common_words['frequency'])
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)
#
#         #emoji analysis
#         st.title("Most Emojis Used")
#         emoji_df = helperClass.emoji_analysis(selected_user, df)
#
#         col1, col2, col3 = st.columns(3)
#
#         with col1:
#             st.dataframe(emoji_df)
#
#         with col2:
#             fig,ax = plt.subplots()
#             ax.pie(emoji_df['frequency'].head(), labels=emoji_df['emojis'].head(), autopct="%1.1f%%")
#             st.pyplot(fig)
#
#         with col3:
#             fig, ax = plt.subplots()
#             ax.bar(emoji_df['emojis'].head(), emoji_df['frequency'].head())
#             plt.ylabel("No. of Times Emoji Used")
#             plt.xlabel("Emojis")
#             st.pyplot(fig)
#
#         # timeline analysis
#         st.title("Monthly TimeLine")
#         timeline = helperClass.timeline_analysis(selected_user, df)
#         fig, ax = plt.subplots()
#         ax.plot(timeline['time'], timeline['message']                                                   , color='red')
#         plt.xticks(rotation='vertical')
#         st.pyplot(fig)
