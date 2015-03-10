import urllib, urllib2
import json
import sys

api_key = "7b4d4b32c605d5f4a7a6484a77231d"
root_url = "https://api.meetup.com/20LetsHang/events/"
keysign = "&key=" + api_key + "&sign=true"
attendance_url = "/attendance?" + keysign
event_host = dict() # maps event id to the host(s) id
attended = dict() # maps people to who first timers they brought

def get_attendance_for_event(id):
    "Gets the people who attended for given id meetup event"
    url = root_url + str(id) + attendance_url + keysign
    u = urllib.urlopen(url)

    info = json.load(u)
    for i in info:
        if i['status'] == "attended":
            if i['member']['name'] not in attended:
                attended[i['member']['name']] = []
                for h in event_host[id]:
                    new = list(attended[h])
                    new.append(i['member']['name'])
                    attended[h] = new

def get_all_events():
    "Gets all the event id's in LetsHang along with its host"
    all_events_url = "https://api.meetup.com/2/events?&photo-host=public&group_urlname=20LetsHang&fields=event_hosts,id&status=past" + keysign
    info = json.load(urllib.urlopen(all_events_url))
    for i in info['results']:
        if "event_hosts" in i:
            for h in i['event_hosts']:
                if i['id'] not in event_host:
                    event_host[i['id']] = [h['member_name']]
                else:
                    new = list([event_host[i['id']]])
                    new.append(h['member_name'])
                    event_host[i['id']] = new

                if h['member_name'] not in attended:
                    attended[h['member_name']] = []

                get_attendance_for_event(i['id'])
    f = open("data.txt", "w")
    f.write(str(attended))

if  __name__ == '__main__':
    get_all_events()
