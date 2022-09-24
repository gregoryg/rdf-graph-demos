# first 50% of users are inactive, rest are active
from faker import Faker
import csv
from random import seed, randint, sample, randrange
from timeit import default_timer as timer
from datetime import timedelta, datetime
# fake = Faker(['en_us', 'pt_pt', 'pt_br', 'es_es', 'it'])
fake = Faker(['en_us'])

def random_date(start, end):
    """
    This function will return a random datetime between two datetime objects
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

def generate_users (numrecords: int, active_only: bool):
    if not active_only:
        user_cnt = numrecords
        records = range(numrecords)
        user_type = "active and inactive"
    else:
        user_cnt = round(numrecords / 2)
        records = range(user_cnt, numrecords)
        user_type = "active"

    starter = timer()
    headers = ["id", "cpf", "name", "gender", "active_date", "active", "address", "city", "state"]
    with open("data/all-active/gjg-users.csv", "wt") as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        for i in records:
            gender = ["M", "F"][randint(0,1)]
            full_name = fake.name_male() if gender=="M" else fake.name_female()
            address = fake.address().split("\n")
            active_date = fake.date_time_between(start_date="-4y", end_date = "now")
            writer.writerow({
                "id": i,
                "cpf": fake.cpf(),
                "name": full_name,
                "gender": gender,
                "active_date": active_date.strftime("%Y-%m-%d"),
                # "active_date": "OHAI",
                "active": int(i > numrecords / 2),
                "address": address[0],
                "city": address[1],
                "state": address[2].split("/ ")[1]
            })
    ender = timer()
    print("Wrote {numlines:,} {usertype} users to data/gjg-users.csv in {thetime}".format(usertype=user_type,numlines=user_cnt,thetime=timedelta(seconds=ender-starter)))
def generate_foaf(numrecords: int, active_only: bool):
    if not active_only:
        user_cnt = numrecords
        records = range(numrecords)
        user_type = "active and inactive"
    else:
        user_cnt = round(numrecords / 2)
        records = range(user_cnt, numrecords)
        user_type = "active"

    starter = timer()
    headers = ["user1_id", "user2_id"]
    rowcnt = 0
    with open("data/all-active/gjg-foaf.csv", "wt") as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=["user1_id", "user2_id"])
        writer.writeheader()
        for i in records:
            friends = []
            friendliness = randint(1,100)
            # simplify by making friend links only to active user range
            # friendliness < 10 ain't got nobody
            if friendliness >= 10 and friendliness <= 99: # normal person
                friends = sample(range(user_cnt, numrecords), randint(1, 24))
            else:
                # friends = sample( range(0, user_cnt - 1), randint( round ((user_cnt - 1) * .00007),  round((user_cnt - 1) * .00028)))
                friends = sample( range(user_cnt, numrecords), randint(42,123))
            for j in friends:
                writer.writerow({
                    "user1_id": i,
                    "user2_id": j
                })
                rowcnt+=1
    ender = timer()
    print("Wrote {rows:,} friends-of-friends rows for {numlines:,} {usertype} users to data/gjg-foaf.csv in {thetime}".format(usertype=user_type,rows=rowcnt,numlines=user_cnt,thetime=timedelta(seconds=ender-starter)))

def generate_p2p_payments(numrecords: int, active_only: bool):
    if not active_only:
        user_cnt = numrecords
        records = range(numrecords)
        user_type = "active and inactive"
    else:
        user_cnt = round(numrecords / 2)
        records = range(user_cnt)
        user_type = "active"
    starter = timer()
    headers = ["tx_id","from_id", "to_id", "payment_timestamp", "wallet_amt", "cc_amt", "total_amt"]
    rowcnt = 0
    with open("data/all-active/gjg-p2p-payments.csv", "wt") as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=headers)
        writer.writeheader()
        tx_id = 1
        d1 = datetime.strptime("2019-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        d2 = datetime.strptime("2022-09-22 00:00:00", "%Y-%m-%d %H:%M:%S")
        for i in records:
            payments = []
            friendliness = randint(1,100)
            # simplify by making payment links only to active user range
            # friendliness < 10 ain't paid nobody
            if friendliness >= 10 and friendliness <= 99: # normal person
                payments = sample(range(user_cnt, numrecords), randint(1, 12))
            else:
                # payments = sample( range(0, user_cnt - 1), randint( round ((user_cnt - 1) * .00007),  round((user_cnt - 1) * .00028)))
                payments = sample( range(user_cnt, numrecords), randint(28,234))
            for j in payments:
                xamt = randint(1000,4200000)
                writer.writerow({
                    "tx_id": tx_id,
                    "from_id": i,
                    "to_id": j,
                    "payment_timestamp": random_date(d1,d2).strftime("%Y-%m-%dT%H:%M:%S"),
                    "wallet_amt": xamt,
                    "cc_amt": 0,
                    "total_amt": xamt
            })
                rowcnt+=1
                tx_id+=1
    ender = timer()

    print("Wrote {rows:,} p2p-payments rows from {usercnt:,} {usertype} users to data/gjg-p2p-payments.csv in {thetime}".format(rows=rowcnt,usercnt=user_cnt,thetime=timedelta(seconds=ender-starter),usertype=user_type))


record_cnt = 100000
generate_users(record_cnt, True)
generate_foaf(record_cnt, True)
generate_p2p_payments(record_cnt, True)
