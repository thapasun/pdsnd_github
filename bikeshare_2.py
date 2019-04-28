import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city=input("\nWhich city data would you like to investigate? chicago,new York city or washington?\n").lower()
        if city in ['chicago','new york city','washington']:
            break
        else:
            print('Your choice is invalid.Please enter a valid city.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month=input("\nWhich month would you like to filter by?\njanuary,february,march,april,may,june or enter 'all' to apply no month filter\n").lower()
        if month in ['january','february','march','april','may','june','all']:
            break
        else:
            print('your choice is invalid.')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day=input("\nWhich day of the week would you like to filter by? \nsunday,monday,tuesday,wednesday,thursday,friday,saturday,or select 'all' to apply no filter.\n").lower()
        if day in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all']:
            break
        else:
            print("your choice is invalid.")

    print('-'*40)
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
    df=pd.read_csv(CITY_DATA[city])
    # convert the Start time to datetime
    df['Start Time']=pd.to_datetime(df['Start Time'])
    # Extract month and day of week from Start Time to create new columns
    df['month']=df['Start Time'].dt.month
    df['day_of_week']=df['Start Time'].dt.weekday_name
     # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('\nThe most common month of travel:',df['month'].mode()[0])

    # display the most common day of week
    print('\nThe most common day of travel:',df['day_of_week'].mode()[0])


    # display the most common start hour
    df['hour'] =df['Start Time'].dt.hour
    print('\n The most common start hour:',df['hour'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station=df['Start Station']
    print('\n The most commonly used start station:',start_station.value_counts().idxmax())

    # display most commonly used end station
    end_station=df['End Station']
    print('\n The most commonly used end station:',end_station.value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    frequent_combination=(start_station+","+end_station).value_counts().idxmax()
    print("\nFrequently used start station:{} and end station:{}.".format(frequent_combination.split(',')[0],frequent_combination.split(',')[1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()



    # display total travel time
    print('\nTotal travel time is {} days'.format(df['Trip Duration'].sum()/86400))

    # display mean travel time
    print("\nMean travel time {} seconds.".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nUser Types count:",df['User Type'].value_counts())

    # Display counts of gender
    # Washington deos not have gender data ,so this code checks for gender in colunm
    if 'Gender' in df.columns:
        print('\n Gender counts:',df['Gender'].value_counts())


    # Display earliest, most recent, and most common year of birth
    # Washington deos not have birth year data, so this code checks for birth year in colunm
    if 'Birth Year' in df.columns:
        print("\n The earliest date of birth:",int(df['Birth Year'].min()))
        print('\n The most recent date of birth:',int(df['Birth Year'].max()))
        print('\n The most common year of birth:',int(df['Birth Year'].mode()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def raw_data_view(df):
    """Display five lines of raw data and prompt the user to see 5 more data until the answer is no."""
    raw_data=input("\n Do you like to see the first 5 lines of raw data?Answer 'yes' or 'no'?\n").lower()

    N=0
    while True:
        if raw_data=='no':
            return

        if raw_data=='yes':

            print(df.iloc[N:N+5,:])
            N=N+5

        raw_data=input("\nWould you like to see 5 more raw data?Answer 'yes' or 'no'\n").lower()





def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_view(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
