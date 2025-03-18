import time
import pandas as pd
import click

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTHS = ('january', 'february', 'march', 'april', 'may', 'june')
WEEKDAYS = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')

def get_user_choice(prompt, choices=('y', 'n')):
    """Prompt user for a valid choice from given options."""
    while True:
        user_input = input(prompt).lower().strip()
        if user_input == 'end':
            raise SystemExit
        if ',' not in user_input:
            if user_input in choices:
                return user_input
        else:
            user_input = [i.strip().lower() for i in user_input.split(',')]
            if all(option in choices for option in user_input):
                return user_input
        prompt = "\nInvalid input. Please enter a valid option:\n>"

def get_filters():
    """Get user input for city, month, and day filters."""
    print("\nLet's explore some US bikeshare data!\n")
    print("Type 'end' anytime to exit the program.\n")
    
    while True:
        city = get_user_choice("\nSelect city(ies) (New York City, Chicago, Washington). Use commas to list multiple:\n>", CITY_DATA.keys())
        month = get_user_choice("\nSelect month(s) (January to June). Use commas to list multiple:\n>", MONTHS)
        day = get_user_choice("\nSelect weekday(s). Use commas to list multiple:\n>", WEEKDAYS)
        
        confirmation = get_user_choice(f"\nConfirm filters:\n City(ies): {city}\n Month(s): {month}\n Weekday(s): {day}\n [y] Yes [n] No\n>")
        if confirmation == 'y':
            break
        print("\nLet's try again!")
    
    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """Load and filter data based on user input."""
    print("\nLoading data...")
    start_time = time.time()
    
    df = pd.concat([pd.read_csv(CITY_DATA[c]) for c in (city if isinstance(city, list) else [city])], sort=True)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.day_name()
    df['Start Hour'] = df['Start Time'].dt.hour
    
    df = df[df['Month'].isin([MONTHS.index(m) + 1 for m in (month if isinstance(month, list) else [month])])]
    df = df[df['Weekday'].isin([d.title() for d in (day if isinstance(day, list) else [day])])]
    
    print(f"\nData loaded in {time.time() - start_time:.2f} seconds.")
    print('-' * 40)
    return df

def display_time_stats(df):
    """Display time-related statistics."""
    print('\nMost frequent times of travel:\n')
    print(f"Most common month: {MONTHS[df['Month'].mode()[0] - 1].title()}")
    print(f"Most common day: {df['Weekday'].mode()[0]}")
    print(f"Most common start hour: {df['Start Hour'].mode()[0]}")
    print('-' * 40)

def display_station_stats(df):
    """Display most popular stations and trips."""
    print('\nMost popular stations and trips:\n')
    print(f"Most common start station: {df['Start Station'].mode()[0]}")
    print(f"Most common end station: {df['End Station'].mode()[0]}")
    df['Route'] = df['Start Station'] + ' - ' + df['End Station']
    print(f"Most common route: {df['Route'].mode()[0]}")
    print('-' * 40)

def display_trip_duration_stats(df):
    """Display trip duration statistics."""
    print('\nTrip Duration Statistics:\n')
    total_duration = df['Trip Duration'].sum()
    mean_duration = df['Trip Duration'].mean()
    print(f"Total travel time: {total_duration // 86400}d {total_duration % 86400 // 3600}h {total_duration % 3600 // 60}m {total_duration % 60}s")
    print(f"Average travel time: {mean_duration // 60}m {mean_duration % 60}s")
    print('-' * 40)

def display_user_stats(df, city):
    """Display statistics on bikeshare users."""
    print('\nUser Statistics:\n')
    print(df['User Type'].value_counts().to_string())
    
    if 'Gender' in df:
        print('\nGender distribution:\n', df['Gender'].value_counts().to_string())
    else:
        print(f"No gender data available for {city.title()}.")
    
    if 'Birth Year' in df:
        print(f"\nEarliest birth year: {int(df['Birth Year'].min())}")
        print(f"Most recent birth year: {int(df['Birth Year'].max())}")
        print(f"Most common birth year: {int(df['Birth Year'].mode()[0])}")
    else:
        print(f"No birth year data available for {city.title()}.")
    print('-' * 40)

def display_raw_data(df):
    """Display raw data upon user request."""
    start = 0
    while True:
        print(df.iloc[start:start+5])
        start += 5
        if get_user_choice("\nShow more raw data? [y] Yes [n] No\n>") != 'y':
            break

def main():
    while True:
        click.clear()
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        while True:
            option = get_user_choice("\nChoose an option:\n [1] Time Stats\n [2] Station Stats\n [3] Trip Duration Stats\n [4] User Stats\n [5] Show Raw Data\n [6] Restart\n>", ('1', '2', '3', '4', '5', '6'))
            click.clear()
            if option == '1':
                display_time_stats(df)
            elif option == '2':
                display_station_stats(df)
            elif option == '3':
                display_trip_duration_stats(df)
            elif option == '4':
                display_user_stats(df, city)
            elif option == '5':
                display_raw_data(df)
            elif option == '6':
                break
        
        if get_user_choice("\nRestart? [y] Yes [n] No\n>") != 'y':
            break

if __name__ == "__main__":
    main()