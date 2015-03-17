import urllib, urllib2
import json
import sys
import re
import time
from igraph import *
import cairo
import operator

api_key = "7b4d4b32c605d5f4a7a6484a77231d"
root_url = "https://api.meetup.com/20LetsHang/events/"
index = 0
keysign = "&key=" + api_key + "&sign=true"
attendance_url = "/attendance?" + keysign
event_host = dict() # maps event id to the host(s) id
attended = dict() # maps people to who first timers they brought
g = ""
vid = dict()

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

def alphabatize():
    "Alphabatizes the members and reformats into a readable file"
    dictlist = []
    for key, value in attended.iteritems():
        temp = [key,value]
        dictlist.append(temp)
    dictlist.sort()
    dictlist = re.sub("\],", "\n", str(dictlist))
    dictlist = re.sub("\', \[u\'", ": ", str(dictlist))
    dictlist = re.sub("\']", "", str(dictlist))
    dictlist = re.sub("\[u\'", "", str(dictlist))
    dictlist = re.sub("\[\]", "", str(dictlist))
    dictlist = re.sub("u\'", "", str(dictlist))
    dictlist = re.sub("\'", "", str(dictlist))
    dictlist = re.sub("\[", "", str(dictlist))
    dictlist = re.sub(", \n", "\n", str(dictlist))
    dictlist = re.sub(", ]]", "", str(dictlist))
    f = open(time.strftime("%y%m%d") + "members.txt", "w")
    f.write("Total number of members: " + str(len(vid.keys())) + "\n\n")
    f.write(str(dictlist))
    f.close()
    
def drawGraph():
    print sorted(vid.items(), key=operator.itemgetter(1))
    g.vs["label"] = g.vs["name"]
    layout = g.layout_kamada_kawai()
    plot(g, layout=layout)
    
if  __name__ == '__main__':
    g = Graph()
    get_all_events()
    alphabatize()
    drawGraph()
