# # from apscheduler.schedulers.background import BackgroundScheduler

# import collections
# import requests
# from bs4 import BeautifulSoup

# # timetabke table table-striped
# # id = timetable

# url = "https://www.edarabia.com/prayer-times-bahrain/"
# page = requests.get(url)
# soup = BeautifulSoup(page.content, "html.parser")
# # results gets timings for the month
# results = soup.find(id="timetable")

# # timings gets timing rows
# timings = results.find_all("tr", class_="")

# # print(type(timings))

# for time in timings:
#     time_to_string = collections.defaultdict(set)
#     print(type(time))
#     splitter = str(time.split("m"))
#     print(splitter.text, end="\n"*2)


# # print(results.prettify())
# # def adhan_scraper():
# #     pass



# # scheduler = BackgroundScheduler()
# # scheduler.add_job(adhan_scraper, 'interval', hours=24)
# # scheduler.start()

import collections

import dateparser               # pip install dateparser
import requests
from bs4 import BeautifulSoup


url = "https://www.edarabia.com/prayer-times-bahrain/"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="timetable")


rows = results.find_all("tr", class_="")
collected_times = set()
for r in rows:
    timings = r.find_all("td", class_="")
    for index, t in enumerate(timings):
        date, *times = timings
        for t in times:
            dt = dateparser.parse(f"{date.text} {t.text}")
            collected_times.add(dt)

times_by_day = collections.defaultdict(list)
for t in sorted(collected_times):
    times_by_day[t.date()].append(t.time())

for day, times in sorted(times_by_day.items()):
    times = [str(t) for t in sorted(times)]
    print(f"{day}:", ", ".join(times))