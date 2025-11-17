import csv
from datetime import datetime, timedelta

# load csv to dictionary
def voyage_schedule(first=False) -> dict:
    schedule = {}
    with open('file/captain_data.csv', 'r') as f:
        csv_reader = csv.reader(f, delimiter='|')
        for i in csv_reader:
            schedule.update({i[1][0]+i[0]:{'name':i[1], 'depart_port':i[2], 'arrive_port':i[3], 'depart_time':i[4], 'arrive_time':i[5]}})
    if first:
        print('Ship schedule loaded.....')
    else:
        for key,value in schedule.items():
            print(f'Captain {value['name']} is scheduled to depart from port {value['depart_port']} on {value['depart_time']}\nThe ship is scheduled to arrive in {value['arrive_port']} on {value['arrive_time']}')
    return schedule


# input captain id and display it's corresponding value
def display_time(schedule: dict):
    captain_id = input("Type the captain number for the port and start date/time you are wanting to see?")
    if captain_id in schedule.keys():
        print(f'Captain {schedule[captain_id]['name']} has a scheduled voyage to {schedule[captain_id]['depart_port']} on {schedule[captain_id]['depart_time']}')
    else:
        print(f'Sorry, captain {captain_id} does not exist / no voyage scheduled')


# do some calculation with time
def voyage_length_time(depart_time: str, arrive_time: str) -> int:
    difference = 0
    depart_hour = datetime.strptime(depart_time, '%Y-%m-%d %H:%M:%S')
    arrive_hour = datetime.strptime(arrive_time, '%Y-%m-%d %H:%M:%S')
    difference += (arrive_hour.hour - depart_hour.hour)
    return difference



def captain_voyages(schedule: dict) -> tuple:
    captain_id = (input("What is the captain id for the voyage that you want to modify the time for?"))
    depart_time, arrive_time = schedule[captain_id]['depart_time'], schedule[captain_id]['arrive_time']
    duration = voyage_length_time(depart_time, arrive_time)
    print(f'The duration of the voyage is {duration} hour')

    time = int(input("Enter how many hour(s) it should increase / decrease by"))
    inc_dec = input("Would this be (i)increase or (d)decrease?")
    details = captain_id, time, inc_dec.lower()
    return details


# calculation with time increase and decrease by using timedelta
def arrival_changes(details: tuple, schedule: dict) -> dict:
    arrival = datetime.strptime(schedule[details[0]]['arrive_time'], '%Y-%m-%d %H:%M:%S')
    match details[2]:
        case 'i':
            arrival = arrival + timedelta(hours=details[1])
        case 'd':
            arrival = arrival - timedelta(hours=details[1])
    schedule[details[0]]['arrive_time'] = datetime.strftime(arrival, '%Y-%m-%d %H:%M:%S')
    print(f'The trip for {schedule[details[0]]['name']} from {schedule[details[0]]['depart_port']} to {schedule[details[0]]['arrive_port']} has changed and now arrives at {schedule[details[0]]['arrive_time']}')
    return schedule

# load csv to dictionary
def load_weather() -> list:
    weather_data = []
    with open('weather_data.csv','r') as file:
        csv_reader = csv.reader(file, delimiter=';')
        for i in csv_reader:
            weather_item  = {'port':i[0], 'date_time':i[1],'temp':i[2], 'wind_speed':i[3],'condition':i[4]}
            weather_data.append(weather_item)
    return weather_data

# check depart ok or arrive ok
def verify_conditions(weather_data: list, schedule: dict):
    min_temp = 5
    max_wind_speed = 30

    captain_id = input("Please enter a captain id to verify weather conditions for the trip")
    depart_ok = False
    arrive_ok = False

    if captain_id in schedule.keys():
        scheduled_arrive_time = datetime.strptime(schedule[captain_id]['arrive_time'], '%Y-%m-%d %H:%M:%S')
        scheduled_depart_time = datetime.strptime(schedule[captain_id]['depart_time'], '%Y-%m-%d %H:%M:%S')
        captain_deport_port = schedule[captain_id]['depart_port']
        captain_arrive_port = schedule[captain_id]['arrive_port']

        for weather in weather_data:
            weather_int_time = datetime.strptime(weather['date_time'], '%Y-%m-%d %H:%M:%S')

            if captain_deport_port in weather['port'] and scheduled_depart_time.date() == weather_int_time.date():
                if int(weather['temp']) < min_temp or int(weather['wind_speed']) > max_wind_speed:
                    print(f'Weather unstable in  {captain_deport_port}: temperature too low / wind speed too high')
                    print(f'The weather today in {captain_deport_port} on the {weather['date_time']} is {weather['condition']}')
                    depart_ok = False

                else:
                    print(f'Suitable weather condition for today\'s voyage from {captain_deport_port}')
                    print(f'The weather today in {captain_deport_port} on the {weather['date_time']} is {weather['condition']}')
                    depart_ok = True

            if captain_arrive_port in weather['port'] and scheduled_arrive_time.date() == weather_int_time.date():
                if int(weather['temp']) < min_temp or int(weather['wind_speed']) > max_wind_speed:
                    print(f'Weather unstable in  {captain_arrive_port}: temperature too low / wind speed too high')
                    print(f'The weather today in {captain_arrive_port} on the {schedule[captain_id]['depart_time']} is {weather['condition']}')
                    arrive_ok = False

                else:
                    print(f'Suitable weather condition for today\'s voyage from {captain_arrive_port}')
                    print(f'The weather today in {captain_arrive_port} on the {schedule[captain_id]['depart_time']} is {weather['condition']}')
                    arrive_ok = True

        if not depart_ok and not arrive_ok:
            print('URGENT: This voyage cannot proceed')
        elif depart_ok and arrive_ok:
            print(f'The voyage from {captain_deport_port} to {schedule[captain_id]['arrive_port']} scheduled for the {schedule[captain_id]['depart_time']} can proceed. No unstable weather')
        else:
            print('Unstable condition further decisions before heading out on the voyage')


def main():
    schedule = voyage_schedule(True)
    while True:
        print('-------------------------------------')
        choice = int(input("Scheduling of Captains & Voyages\n"
                           "1. Show voyage schedule prior to any updates\n"
                           "2. Check voyage start time for a captain\n"
                           "3. Voyage schedule time adjustments\n"
                           "4. Weather verification and detection for voyage safety\n"
                           "5. Exit\n"))
        match choice:
            case 1:
                voyage_schedule(False)
            case 2:
                display_time(schedule)
            case 3:
                details = captain_voyages(schedule)
                schedule = arrival_changes(details, schedule)
            case 4:
                weather_data = load_weather()
                verify_conditions(weather_data, schedule)
            case 5:
                break
            case _:
                print("Incorrect choice entered")


if __name__ == '__main__':
    main()