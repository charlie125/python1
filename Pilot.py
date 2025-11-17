import csv
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime
from os.path import split


def flight_schedule(first=False) -> dict:
        schedule = {}
        with open('pilot_data.csv', 'r') as f:
            reader = csv.reader(f, delimiter=';')
            for i in reader:
                key = 'pilot'+ i[0]
                schedule.update({key:{'name': i[1], 'flight_id': i[2], 'coord':i[3], 'start_time':i[4], 'end_time':i[5]}})
        if first:
            print('Flight schedule loaded.....')
        else:
            for key1, value1 in schedule.items():
                print(f'Pilot {key1} name is {value1['name']} they are scheduled to fly on {value1['start_time']}')
        return schedule


def display_flight_time(schedule: dict):
    pilot_id = input("Type the pilot id for the start date/time are you wanting to see?")
    if pilot_id in schedule.keys():
        print(f'{schedule[pilot_id]['name']} has a scheduled flight for {schedule[pilot_id]['start_time']}')
    else:
        print(f'Sorry, {pilot_id} does not exist / no flight scheduled.')

def validate_time(check_in_time: str) -> bool:
    try:
        #complete the call to strptime() on the next line
        datetime.strptime(check_in_time, '%H:%M:%S')
        return True
    except ValueError:
        print("Invalid time format")
        return False


def check_in(pilot_id: str, schedule: dict, time_checked_in: str):
    time_checked_in = datetime.strptime(time_checked_in, '%H:%M:%S')
    if pilot_id in schedule.keys():
        converted_time = datetime.strptime(schedule[pilot_id]['start_time'], '%Y-%m-%d %H:%M:%S')
        if time_checked_in.time() < converted_time.time():
            print('You have checked in successfully')
        else:
            return logging_late_check_in(pilot_id)


def logging_late_check_in(pilot_id: str):
    print('You logged in late')
    msg = "checked in late"
    with open ('late_checkin.csv', 'a') as f:
        f.write(f'{pilot_id} {msg};\n')


# Haversine formula to calculate distance between two sets of coordinates (in kilometers)
def haversine(coord1: str, coord2: str) -> float:
    lat1, lon1 = map(float, coord1.split(','))
    lat2, lon2 = map(float, coord2.split(','))

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    R = 6371  # Radius of Earth in kilometers
    distance = R * c

    return distance


def detect_conflict(pilot1: str, pilot2: str, schedule: dict):
    coord1, coord2 = schedule[pilot1]['coord'], schedule[pilot2]['coord']
    flightId1, flightId2 = schedule[pilot1]['flight_id'], schedule[pilot1]['flight_id']
    start_time1, start_time2 = schedule[pilot1]['start_time'], schedule[pilot2]['start_time']

    distance = haversine(coord1, coord2)

    if distance < 500 and start_time1 == start_time2:
        print(f'Conflict detected between pilot {pilot1}({flightId1}) and pilot {pilot2}({flightId2}) at {coord1},{coord2}. Distance: {distance:.2f} km')
    else:
        print('No conflict detected')


def main():
    schedule = flight_schedule(first=True)
    while True:
        choice = int(input("Flight Control & Scheduling of Pilots\n"
                           "1. Show flight schedule\n"
                           "2. Check flight start time for a pilot\n"
                           "3. Pilot check in\n"
                           "4. Detect conflict for flights\n"
                           "5. Exit\n"))
        match choice:
            case 1:
                flight_schedule(first=False)
            case 2:
                display_flight_time(schedule)
            case 3:
                pilot_id = input("Please enter the pilot's id for check in")
                check_in_time = input("What time are they checking in?")
                validated = validate_time(check_in_time)
                if not validated:
                    print('The time that you have entered is not in the correct format. Enter it as HH:MM:SS')
                    print('')
                else:
                    check_in(pilot_id, schedule, check_in_time)
                """
                complete the if/else code here to give an error if time is invalid or call check_in() 
                the check_in() can be seen here below these comments
                """

            case 4:
                pilot_id1 = input("Please enter the pilot's id")
                pilot_id2 = input("Please enter the second pilot's id")
                detect_conflict(pilot_id1, pilot_id2, schedule)
            case 5:
                break
            case _:
                print("Incorrect choice entered")


if __name__ == '__main__':
    main()
