#!/usr/bin/env python
# coding: utf-8

# # Analysis of Free Mobile Applications and Ad Revenue
# 
# The purpose of this project is to analyze the current offering of applications in both the Apple and Android app stores, in an effort to help developers understand what apps are likely to attract more users.
# 
# Beyond the goal of user attraction, we are also interested to see what users, and how many, both see and engage in in-app ads. The purpose of this information is to guide development decisions to maximize ad revenue and product usage.

# In[3]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# In[4]:


from csv import reader
apple_store = open('c:\\users\\daxto\\Jupyter DataSets\\AppleStore.csv', encoding='utf8')
applestoredata = reader(apple_store)
apple_data = list(applestoredata)
google_play = open('c:\\users\\daxto\\Jupyter DataSets\\googleplaystore.csv', encoding='utf8')
googlestoredata = reader(google_play)
google_data = list(googlestoredata)


# In[5]:


explore_data(apple_data,1,3,True)


# In[6]:


explore_data(google_data,1,3,True)


# ## Getting Familiar
# 
# Through the explore_data function, we have been able to see what the table looks like and what we can expect from each column. 
# 
# Below is printed the column headers for each data set. If any questions arise about the columns, we can refer back to the documentation for either the [Apple Store](https://www.kaggle.com/datasets/ramamet4/app-store-apple-data-set-10k-apps) or [Google Store](https://www.kaggle.com/datasets/lava18/google-play-store-apps) data sets.

# In[7]:


print(apple_data[0])
print('\n')
print(google_data[0])


# # Data Cleaning
# An error was reported in the discussion section saying that there is a wrong entry for 10472. They said that the entry is missing a rating column and shifted everything over as a result.

# In[8]:


print(google_data[10473])
print('\n')
print(google_data[0])
print('\n')
print(google_data[1])


# In[9]:


print(len(google_data))
del google_data[10473]
print(len(google_data))


# In[10]:


print(google_data[10473])
del google_data[10473]


# # Do Not Run Anything Above This

# ## Testing for Duplicates

# Now we want to test for duplicate entries. The Google Play dataset has duplicate entries of many apps including Instagram.

# In[11]:


for app in google_data[1:]:
    name = app[0]
    if name == 'Instagram':
        print(app)
    


# We have confirmed many duplicates in the data set. To combat this we have created two lists, one for unique names and one for duplicate names. The loop underneath this checks to see if the name is already listed in the unique list, if not it appends to the unique list. If it is found in the unique list, it appends to the duplicate app names. 

# In[12]:


unique_google_apps = []
duplicate_google_apps = []

for app in google_data[1:]:
    name = app[0]
    if name in unique_google_apps:
        duplicate_google_apps.append(name)
    else:
        unique_google_apps.append(name)

print('Number of duplicate apps:', len(duplicate_google_apps))
print('Number of unique apps:', len(unique_google_apps))
print('\n')
print('Example of duplicates:', duplicate_google_apps[:10])


# We won't remove duplicates at random, it's important to understand what might be different. In this case it's number of reviews as the data was collected. We will want to keep the most reviews an app received.

# In[13]:


del google_data[10473]


# In[14]:


reviews_max = {}

for app in google_data[1:]:
    name = app[0]
    n_reviews = float(app[3])
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
        
    elif name not in reviews_max:
        reviews_max[name] = n_reviews


# Checking length of dictionaries and lists to match up.

# In[15]:


print(len(reviews_max))


# In[16]:


android_clean = []
already_added = []

for app in google_data[1:]:
    name = app[0]
    n_reviews = float(app[3])
    
    if (n_reviews == reviews_max[name]) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)


# After cleaning the google data, I realized that my naming convention wasn't consistent with the lists. In addition, I kept the column headers in the lists up to this point. In the cell below, I have created a new list called ```apple_clean``` which is the apple list without column headers.

# In[17]:


apple_clean = []
for row in apple_data[1:]:
    apple_clean.append(row)


# Checking and viewing data

# In[18]:


explore_data(android_clean, 0, 3, True)


# After exploring the data, we can confirm that the number of rows is correct and that the duplicates we previously found have been removed.

# ## Removing Non-English Apps

# To check for non-english characters, we can use the function ord() to retreive the ASCII number value for the character. English commonly uses characters with the value 0-127. We can build a function to check for those.

# In[19]:


def is_english(string):
    non_en_char_count = 0
    
    for char in string:
        if ord(char) > 127:
            non_en_char_count += 1
            
    if non_en_char_count > 3:
        return False
    else:
        return True


# We are testing the function on the following strings:

# In[20]:


print(is_english('Instagram'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))


# It's clear that some primarly english apps use emojis or other characters that don't pass our function that should be kept. For this reason, we will only remove apps that have more than three non-standard english characters. 
# 
# Changes were made inthe function to include the count for ```non_en_char_count```

# New lists titled ```apple_english``` and ```android_english``` will be used to get the latest cleaned data.

# In[21]:


apple_english = []
android_english = []


# We now need to use the function to filter out any non-english apps in both the ```android_clean``` and ```apple_clean```

# In[22]:


for row in android_clean:
    title = row[0]
    if is_english(title):
        android_english.append(row)
        
for row in apple_clean:
    title = row[2]
    if is_english(title):
        apple_english.append(row)


# Checking our work now

# In[23]:


explore_data(android_english, 0, 2, True)
print('\n')
explore_data(apple_english, 0, 2, True)


# ## Isolating the Free Apps

# In this section we would like to isolate the data to only include free applications. After this we will verify the data is clean. If it is, this is the last section we will do prior to analysis. Because of this, our list titles will be called ```apple_final``` and ```android_final```
# 
# For ios the price is found in ```apple_english index[7]```
# For andriod, the price is found in ```andriod_english index[5]```

# In[24]:


apple_final = []
android_final = []


# In[25]:


for app in android_english:
    price = app[7]
    if price == '0':
        android_final.append(app)
        
for app in apple_english:
    price = app[5]
    if price == '0':
        apple_final.append(app)


# In[26]:


print(len(android_final))

print(len(apple_final))


# # Analysis

# ## Most Common Apps by Genre
# 
# To minimize risks and overhead, our validation strategy for an app idea has three steps:
# 
# Build a minimal Android version of the app, and add it to Google Play.
# If the app has a good response from users, we develop it further.
# If the app is profitable after six months, we build an iOS version of the app and add it to the App Store.
# Because our end goal is to add the app on both Google Play and the App Store, we need to find app profiles that are successful in both markets. For instance, a profile that works well for both markets might be a productivity app that makes use of gamification.
# 
# Let's begin the analysis by determining the most common genres for each market. For this, we'll need to build frequency tables for a few columns in our datasets.

# Genre can be found in the following columns per dataset:
# 
# ```apple_final index[12]```
# ```android_final index[1]```
# 
# First we create a couple functions to assist in the creation of frequency tables.

# In[27]:


def freq_table(dataset, index):
    freq_table = {}
    total = 0
    
    for row in dataset:
        key = row[index]
        total += 1
        if key not in freq_table:
            freq_table[key] = 1
        else:
            freq_table[key] += 1
    
    table_percent = {}
    for key in freq_table:
        percentage = (freq_table[key] / total) * 100
        table_percent[key] = percentage
        
    return table_percent

def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# In[28]:


display_table(apple_final, 12)


# Apple's App Store is dominated by Games which holds a massive 58% of the share given the criteria we have already specified (free, non-duplicated, english only applications). Interesting to see entertainment follow up games in second place with a solid almost 8%.

# In[29]:


display_table(android_final, 1)


# Google Play's store is very different than the Apple store. Here we see family as the top category, with games at second. However, Games holds a smaller percentage of all apps with a differences of almost a full 50% compared with games in Apple's app store. Let's investigate what family actually means.

# In[30]:


android_family_apps = []
for apps in android_final:
    genre = apps[1]
    if genre == 'FAMILY':
        android_family_apps.append(apps)
        
for row in android_family_apps[:4]:
    print(row)
    print('\n')


# As seen in the data above, family can typically mean a game designed for children or families. This does help to even the large imbalance of genres between our two lists. However, it is obvious that a practicality is favored far more in the Google Play Store than the App Store.

# ## Most Popular App by Genre in Apple App Store

# One way to find out what genres are the most popular (have the most users) is to calculate the average number of installs for each app genre. For the Google Play data set, we can find this information in the Installs column, but this information is missing for the App Store data set. As a workaround, we'll take the total number of user ratings as a proxy, which we can find in the rating_count_tot app which is found on ```index[6]```

# In[31]:


apple_genres = freq_table(apple_final, 12)
print(apple_genres)


# In[32]:


for genre in apple_genres:
    total = 0
    len_genre = 0
    for app in apple_final:
        app_genre = app[12]
        if app_genre == genre:
            num_ratings = float(app[6])
            total += num_ratings
            len_genre += 1
    ave = total / len_genre
    print(genre, ':', ave)


# The most popular apps by genre are found in the navigation and social networking genres. This could be influenced heavily by the amount of reviews people have left. After all, we are using number of reviews left as opposed to actual downloads.

# Music is also relatively popular and could be a good way to catch a lot of users. Navigation and social media are difficult to get into because the players in the space are so big. Many people don't use anything outside of google maps, apple maps, or waze. Social media is likely even more difficult.
# 
# Music could be a great way to go as new ways to interact, share, and listen to music seem to be very popular. Everyone loves sharing their passions, and there is a big user base for it. 

# ## Most Popular Apps by Genre on Google Play

# To start this we will form a frequency table, using our function, to display what the data would look like using ```index[5]``` which is the total number of installs.

# In[33]:


display_table(android_final, 5)


# As we can see, the data is put into buckets with no exact numbers. For our purposes, this is fine, and we will just take each amount as stated. We will consider an app with 10,000+ installs to have just 10,000 and convert that number to a float so that we can group by genre.

# In[49]:


for row in android_final:
    users = row[5]
    users = users.replace('+', '')
    users = users.replace(',', '')
    users = users.replace(' ', '')
    row[5] = float(users)


# In[53]:


android_cat_freq = freq_table(android_clean, 1)


# In[54]:


for category in android_cat_freq:
    total = 0
    len_category = 0
    for app in android_final:
        app_category = app[1]
        total_users = float(app[5])
        if app_category == category:
            total += total_users
            len_category += 1
    ave = total / len_category
    print(category, ':', ave)


# The data is heavily skewed towards communication and social platforms. An investigation of those show this information:

# In[61]:


for row in android_final:
    category = row[1]
    users = row[5]
    name = row[0]
    if category == 'COMMUNICATION':
        print(name, ':', users)


# As shown, the data is blown way out because of apps that have over 1 billion downloads, like WhatsApp. We can assume the same for social media, like in the apple data, because of big players like Facebook, Instagram, Twitter, etc.
# 
# Unfortunately, google does not have a music category. This makes it very difficult to compare to our reccomendation of music applications from the apple list. However, we can pull data on similar categories to test the idea of a music, lifestyle, or productivity centered app.

# In[69]:


for row in android_final:
    category = row[1]
    users = row[5]
    name = row[0]
    if category == 'ENTERTAINMENT':
        print(name, ':', users)


# In[70]:


for row in android_final:
    category = row[1]
    users = row[5]
    name = row[0]
    if category == 'PRODUCTIVITY':
        print(name, ':', users)


# # Conclusions
# 
# In this project, we analyzed data from two large datasets covering the Apple App Store and Google Play Store. After cleaning the data, we determined the frequency and percentage share of each app category to determine what might be popular.
# 
# Though there are many directions you could take the data, we determined there could be an opportunity in the music/productivity space. There are many music players and many social medias. However, there is an opportunity to create a unique feature to attract users. 
# 
# Both apple and android users are big into productivity and family. Features in a music app that could be profitable would be a music app that helps children sleep at night, including a night light on the screen and calming music. Another app that would fit a similar space is a productivity app that can use music to help you focus on a task for a set amount of time/songs. After that amount of time, the user knows it's time to take a break.
