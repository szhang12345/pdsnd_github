
# coding: utf-8

# In[ ]:


import time
import pandas as pd
import numpy as np
import statistics as st
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')

    #lower is used to get input in any format
    # user input for city (chicago, new york, washington)
    city = input('\nWould you like to see data for Chicago, New York, or Washington?\n').lower()
    

    while(True):
        if(city == 'chicago' or city == 'new york' or city == 'washington' or city == 'all'):
            break
        else:
            city = input('Sorry, I don\'t understand, please enter the correct city: ').lower()
           
    # user input for month (all, january, february, ... , june)
    month = input('\nWhich month do you want to review? Please type in January, February, March, April, May, or June?\n').lower()
     

    while(True):
        if(month == 'january' or month == 'february' or month == 'march' or month == 'april' or month == 'may' or month == 'june' or month == 'all'):
            break
        else:
            month = input('Sorry, I don\'t understand, please enter the correct month\n').lower()
    
    # user input for day of week (all, monday, tuesday, ... sunday)
    day =  input('Which day do you want to review? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday , Sunday or all to display data of all days?\n').lower()
   

    while(True):
        
        if(day == 'monday' or day == 'tuesday' or day == 'wednesday' or day == 'thursday' or day == 'friday' or day == 'saturday' or day == 'sunday' or day == 'all'):
            break
        else:
            day = input('Sorry, I don\'t understand, please enter the correct day: ').lower()
  
    # break up sections
    print('*'*50)
    return city, month, day
   
    
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

      # convert date into date format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
   
    df['End Time'] = pd.to_datetime(df['End Time'])
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
     
        month = months.index(month) + 1       

        df = df[df['Start Time'].dt.month == month]
        
    #filter data by day.
    if day != 'all': 
        df = df[df['Start Time'].dt.weekday_name == day.title()]


    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if(month == 'all'):
        common_month = df['Start Time'].dt.month.value_counts().idxmax()
        print('Most common month is ' + str(common_month))

    # display the most common day of week
    if(day == 'all'):
        common_day = df['Start Time'].dt.weekday_name.value_counts().idxmax()
        print('Most common day is ' + str(common_day))

    # display the most common start hour
    common_hour = df['Start Time'].dt.hour.value_counts().idxmax()
    print('Most popular hour is ' + str(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*50)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = st.mode(df['Start Station'])
    print('\nMost common start station is {}\n'.format(common_start_station))

    # display most commonly used end station
    common_end_station = st.mode(df['End Station'])
    print('\nMost common end station is {}\n'.format(common_end_station))

    # display most frequent combination of start station and end station trip
    comb_trip = df.groupby(['Start Station', 'End Station'])
    frequent_trip_count = comb_trip['Trip Duration'].count().max()
    frequent_trip = comb_trip['Trip Duration'].count().idxmax()
    print('Most Frequent trip: {}, {}'.format(frequent_trip[0], frequent_trip[1]))
    print('{0:30}{1} trips'.format(' ', frequent_trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*50)

def popular_trip(df):
    '''Finds and prints the most popular trip.
    Args:
        bikeshare dataframe
    Returns:
        none
    '''
    pd.set_option('max_colwidth', 100)
    df['journey'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    most_pop_trip = df['journey'].mode().to_string(index = False)
    # The 'journey' column is created in the statistics() function.
    print('The most popular trip is {}.'.format(most_pop_trip))

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    time_travel = total_travel_time
    day_travel = time_travel // (24 * 3600)
    time_travel = time_travel % (24 * 3600)
    hour_travel = time_travel // 3600
    time_travel %= 3600
    minutes_travel = time_travel // 60
    time_travel %= 60
    seconds_travel = time_travel
    print('\nTotal travel time is {} days {} hours {} minutes {} seconds'.format(day_travel, hour_travel, minutes_travel, seconds_travel))


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    time_mean_travel = mean_travel_time
    day_mean_travel = time_mean_travel // (24 * 3600)
    time_mean_travel = time_mean_travel % (24 * 3600)
    hour_mean_travel = time_mean_travel // 3600
    time_mean_travel %= 3600
    minutes_mean_travel = time_mean_travel // 60
    time_mean_travel %= 60
    seconds_mean_travel = time_mean_travel
    print('\nMean travel time is {} days {} hours {} minutes {} seconds'.format(day_mean_travel, hour_mean_travel, minutes_mean_travel, seconds_mean_travel))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
     
    # Display counts of user types

    user_types = df['User Type'].value_counts()
    for idx in range(len(user_types)):
        val = user_types[idx]
        user_type = user_types.index[idx]
        print('{0:21}'.format((user_type + ':')), val)



    # Display counts of gender
    if 'Gender' in df.columns:
        
        genders = df['Gender'].value_counts()
        for idx in range(len(genders)):
            val = genders[idx]
            gender = genders.index[idx]
            print('{0:21}'.format((gender + ':')), val)
            
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        
        print('Earliest Year of Birth:        ', int(df['Birth Year'].min()))
        print('Most recent Year of Birth:     ', int(df['Birth Year'].max()))
        print('Most common Year of Birth:     ', int(df['Birth Year'].mode()))
   

  
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('*'*50)

def display_raw_data(df):

    show_row = 5
    start_row = 0
    end_row = show_row - 1

    print('\n    Would you like to see some raw data from the dataset?')
    while True:
        raw_data = input('(yes or no):  ')
        if raw_data.lower() == 'yes':

            print('\nDisplaying rows {} to {}:'.format(start_row + 1, end_row + 1))

            print('\n', df.iloc[start_row : end_row + 1])
            start_row += show_row
            end_row += show_row

            print_line('.')
            print('\n    Would you like to see the next {} rows?'.format(show_row))
            continue
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        popular_trip(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter y or n.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()

