import csv
import sqlalchemy
from sqlalchemy import create_engine
from app import db, app

from app.models import StreetCleaning

def add_street_cleaning_data():

    with open('app/data/sfsweeproutes.csv', 'rU') as csvfile:
        street_cleanings = csv.reader(csvfile, delimiter=',')
        street_cleanings.next()
        print "adding street cleaning data"
        for street_cleaning in street_cleanings:
            # remove :00 in times. 12:00 --> 12
            start_time = street_cleaning[6][:-3]
            end_time = street_cleaning[7][:-3]

            street_min = get_min(street_cleaning)
            street_max = get_max(street_cleaning)

            if street_min == '0' and street_max == '0':
                continue

            # side corresponds to even or odd address. Left = odd (1), Right = even(0)
            side = 1 if street_cleaning[4] == 'L' else 0

            new_street_cleaning = StreetCleaning(
                weekday = street_cleaning[1],
                side = side,
                fromhour = int(start_time),
                tohour = int(end_time),
                holidays = street_cleaning[8],
                week1ofmon = street_cleaning[9],
                week2ofmon = street_cleaning[10],
                week3ofmon = street_cleaning[11],
                week4ofmon = street_cleaning[12],
                week5ofmon = street_cleaning[13],
                street_min = int(street_min),
                street_max = int(street_max),
                streetname = street_cleaning[18]
            )

            db.session.add(new_street_cleaning)
    db.session.commit()

def get_min(street_cleaning):
    if street_cleaning[14] == '0':
        return street_cleaning[17]
    elif street_cleaning[17] == '0':
        return street_cleaning[14]
    else:
        return min(int(street_cleaning[14]), int(street_cleaning[17]))

def get_max(street_cleaning):
    if street_cleaning[15] == '0':
        return street_cleaning[16]
    elif street_cleaning[16] == '0':
        return street_cleaning[15]
    else:
        return max(int(street_cleaning[15]), int(street_cleaning[16]))

def prune_data():
    # Once all data is inserted:
    # 1. Find all distinct cleanings based on street, weekday, hours, and side
    # 2. for each of those, find all other cleanings that match (without address info)
    # 3. Sort by street_min and combine address information to get one row instead of many
    # Original CSV = 37896 rows. After pruning: 7419 rows

    print "pruning data"
    distinct_cleanings = StreetCleaning.query.distinct(
        StreetCleaning.streetname,
        StreetCleaning.weekday,
        StreetCleaning.fromhour,
        StreetCleaning.tohour,
        StreetCleaning.side,
    ).all()

    cleanings_to_delete = []
    for d in distinct_cleanings:
        cleanings = StreetCleaning.query.filter_by(
            streetname=d.streetname,
            weekday=d.weekday,
            fromhour=d.fromhour,
            tohour=d.tohour,
            side=d.side
        ).order_by(StreetCleaning.street_min).all()

        x = 0
        n = 1
        while n < len(cleanings):
            if cleanings[n].street_min - cleanings[x].street_max < 150:
                # if next row is within next block of current cleaning row, create new max
                # for first row and delete the second
                cleanings[x].street_max = max(cleanings[x].street_max, cleanings[n].street_max)
                cleanings_to_delete.append(cleanings[n])
                n += 1
            else:
                x = n
                n += 1

    for cleaning in cleanings_to_delete:
        db.session.delete(cleaning)
    db.session.commit()

if __name__ == '__main__':
    add_street_cleaning_data()
