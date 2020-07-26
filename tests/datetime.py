import datetime

date = "04/17/2020"


def user_check(dt):
    if dt != datetime.datetime.now().strftime("%m/%d/%Y") or dt == 0:
        now = datetime.datetime.now().strftime("%m/%d/%Y")
    else:
        now = dt
    return now


print(datetime.datetime.now().strftime("%m/%d/%Y"))

command = input('Write a command:\n')
if command == "time":
    date = user_check(date)
    print(date)

command = input('Write a command:\n')
if command == "time":
    date = user_check(date)
    print(date)

print(date)
