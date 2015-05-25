import cairo
from igraph import *
import json
import operator
import re
import sys
import time
import urllib, urllib2

api_key = "7b4d4b32c605d5f4a7a6484a77231d"
root_url = "https://api.meetup.com/20LetsHang/events/"
keysign = "&key=" + api_key + "&sign=true"
attendance_url = "/attendance?" + keysign
event_host = dict() # maps event id to the host(s) id
attended = dict() # maps people to who first timers they brought
g = ""
vid = dict()
total = 0

def get_attendance_for_event(uid, index):
    "Gets the people who attended for given id meetup event"
    url = root_url + str(uid) + attendance_url + keysign
    u = urllib.urlopen(url)
    try:
        info = json.load(u)
        for i in info:
            if i['status'] == "attended":
                if i['member']['name'].strip() == u'T\xf9ng N\u1edd D\xea':
                    i['member']['name'] = u'Tung No De'
                elif i['member']['name'].strip() == u'R\xe9mi':
                    i['member']['name'] = u'Remi'

                if i['member']['name'].strip() not in attended:
                    attended[i['member']['name'].strip()] = []
                    g.add_vertex(i['member']['name'])
                    vid[i['member']['name'].strip()] = index
                    index += 1
                    for h in event_host[uid]:
                        g.add_edge(vid[h], vid[i['member']['name'].strip()])
                        new = list(attended[h])
                        new.append(i['member']['name'].strip())
                        attended[h] = new
    except ValueError:
        print "ValueError for " + url + " !"
    return index

def get_all_events():
    "Gets all the event id's in LetsHang along with its host"
    index = 0
    all_events_url = "https://api.meetup.com/2/events?&photo-host=public&group_urlname=20LetsHang&fields=event_hosts,id&status=past" + keysign
    info = json.load(urllib.urlopen(all_events_url))
    for i in info['results']:
        global total 
        total += 1
        if "event_hosts" in i:
            for h in i['event_hosts']:
                if i['id'] not in event_host:
                    event_host[i['id']] = [h['member_name'].strip()]
                else:
                    new = list([event_host[i['id']]])
                    new.append(h['member_name'].strip())
                    event_host[i['id']] = new

                if h['member_name'].strip() == u'T\xf9ng N\u1edd D\xea':
                    h['member_name'] = u'Tung No De'
                elif h['member_name'].strip() == u'R\xe9mi':
                    h['member_name'] = u'Remi'

                if h['member_name'].strip() not in attended:
                    g.add_vertex(h['member_name'].strip())
                    vid[h['member_name'].strip()] = index
                    index += 1
                    attended[h['member_name'].strip()] = []

                index = get_attendance_for_event(i['id'], index)

def number():
    "Shows how many newbies each member got"
    for key, value in attended.iteritems():
        if len(value) > 0 and "(" not in key:
            attended[key + " (" + str(len(value)) + ")"] = value
            del attended[key]

def alphabatize():
    "Alphabatizes the members and reformats into a readable file"
    dictlist = []
    for key, value in attended.iteritems():
        temp = [key,value]
        dictlist.append(temp)
    dictlist.sort()
    dictlist = re.sub("\', \[u\'", ": ", str(dictlist))
    dictlist = re.sub("\', \[\]\], \[u\'", "\n", str(dictlist))
    dictlist = re.sub("\'\]\], \[u\'", "\n", str(dictlist))
    dictlist = re.sub("\', u\'", ", ", str(dictlist))
    dictlist = re.sub("\', \[\]\]\]", "", str(dictlist))
    dictlist = re.sub("\[\[u\'", "", str(dictlist))
    f = open("/Users/andreawu/Documents/meetupnewbies/members.txt", "w")
    f.write("Total number of distinct attendees: " + str(len(vid.keys())) + "\n")
    f.write("Total number of events: " + str(total) + "\n\n")
    f.write(str(dictlist))
    f.close()
    
def drawGraph():
    g.vs["label"] = g.vs["name"]
    g.vs["color"] = ["blue"]
    layout = g.layout_fruchterman_reingold()
    plot(g, layout=layout, bbox=(1500, 1500), margin=100, vertex_size=1)
    
if  __name__ == '__main__':
    g = Graph()
    get_all_events()
    number()
    alphabatize()
    drawGraph()
