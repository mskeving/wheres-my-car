import csv
import sqlalchemy
from sqlalchemy import create_engine
from app import db, app

from app.model import StreetCleaning

def main():

    with open('sfsweeproutes.csv', 'rU') as csvfile:
        street_cleanings = csv.reader(csvfile, delimiter=',')
        street_cleanings.next()
        for street_cleaning in street_cleanings:
            # remove :00 in times. 12:00 --> 12
            start_time = int(street_cleaning[6][:-3])
            end_time = int(street_cleaning[7][:-3])

            new_street_cleaning = StreetCleaning(
                cnn = int(street_cleaning[0]),
                weekday = street_cleaning[1],
                blockside = street_cleaning[2],
                blocksweep = street_cleaning[3],
                cnnrightle = street_cleaning[4],
                corridor = street_cleaning[5],
                fromhour = start_time,
                tohour = end_time,
                holidays = street_cleaning[8],
                week1ofmon = street_cleaning[9],
                week2ofmon = street_cleaning[10],
                week3ofmon = street_cleaning[11],
                week4ofmon = street_cleaning[12],
                week5ofmon = street_cleaning[13],
                lf_fadd = street_cleaning[14],
                lf_toadd = street_cleaning[15],
                rt_toadd = street_cleaning[16],
                rt_fadd = street_cleaning[17],
                streetname = street_cleaning[18],
                zip_code = street_cleaning[19],
                nhood = street_cleaning[20],
                district = street_cleaning[21],
            )

            db.session.add(new_street_cleaning)
    db.session.commit()

if __name__ == '__main__':
    main()
