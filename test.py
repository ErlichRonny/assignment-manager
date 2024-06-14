from datetime import date

#datetime module
today = date.today()
print("Date: ", today)
print(f"Today is: {today}")
print("Day: ", today.day)
print("Month: ", today.month)
print("Year: ", today.year)

print(today.strftime("%A, %dth of %B %y"))
next_year = today.replace(year = today.year + 1)
print(next_year)

difference = abs(next_year - today)
print("only {} days until next year".format(difference.days))

random_date = date(1856, 7, 10)
print(random_date)
print(random_date.weekday())
