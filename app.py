import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import numpy as np
import mplcyberpunk
import pandas as pd

st.sidebar.title("SP Chat Detective: Uncovering the Secrets of Your WhatsApp Conversations")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.title("The Most Stat-tastic😋 Stats")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # monthly timeline
        st.title("Life in a Nutshell: A Monthly Recap")
        plt.style.use("cyberpunk")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
         # Add Text watermark
        fig.text(0.9, 0.15, 'Sougata Chat Detective', fontsize = 7,
                 color ='grey', ha ='right', va ='top',
                 alpha = 0.7)
        #ax.plot(timeline['time'], timeline['message'],color='green')
        ax.plot(timeline['time'], timeline['message'],marker='o',color='chartreuse')
        # Add glow effects-Optional
        mplcyberpunk.add_glow_effects()
        plt.xticks(rotation='vertical')
        plt.title("Monthly Timeline")
        st.pyplot(fig)

        # daily timeline
        st.title("The Never-Ending Story: A Daily Diary")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'],color='crimson')
        #mplcyberpunk.make_lines_glow()
        plt.xticks(rotation='vertical')
        plt.title("Daily Timeline")
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
            # Most busy day
            st.header("The Day That Wouldn't End: A Tale of Busyness")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='limegreen')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            # Most busy month
            st.header("May-Hem: Surviving the Busiest Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='darkmagenta')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            #Most Busy Users
            st.title('The Busy Bees: A Story of Most Active Users')
            x,new_df = helper.most_busy_users(df)

            colors = ['red','limegreen', 'yellow','hotpink', 'orangered']
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color=colors)
                #ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()
        
        #plt.pyplot.viridis()
        # Horizontal Bar Plot
        bar = ax.barh(most_common_df[0],most_common_df[1])
        plt.tight_layout()
        #ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

        ax.invert_yaxis()
        # Add annotation to bars
    
        for i in ax.patches:
            plt.text(i.get_width()+0.2, i.get_y()+0.5,
            str(round((i.get_width()), 2)),
            fontsize = 8, fontweight ='bold',
            color ='grey')
        plt.xticks(rotation='vertical')
       # Add Text watermark
        fig.text(0.9, 0.15, 'Sougata Chat Detective', fontsize = 12,
                 color ='grey', ha ='right', va ='bottom',
                 alpha = 0.7)
        
        st.title('Word Vomit: The Most Overused Words')
        plt.title("Most commmon words")
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emojinal Rollercoaster: Analyzing Our Favorite Icons")

        plt.rcParams['font.family'] = 'DejaVu Sans'
        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)
            

