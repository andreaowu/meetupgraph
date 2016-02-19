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
event_host = dict()             # key: event id, value: list of host name(s)
attended = dict()               # key: host name, value: list of first timers' names
events_per_member = dict()      # key: member name, value: number of events attended
morethanone = []                # names of members who have been to more than one event
g = ""                          # graph that we will draw out at the end
vid = dict()            
total_events = 0                # total number of events for 20LH

'''
Input:  uid is the meetup event id
        index is the number of people who attended events we so far parsed

Output: total accumulation of attendees

Function also:  adds attendees' names to attended dict
                adds new vertices to g for attendees we haven't seen before
                adds edges to g between hosts and newbies

'''
def get_attendance_for_event(uid, index):
    "Returns the number of attendees for given uid of a meetup event"
    url = root_url + str(uid) + attendance_url + keysign
    u = urllib.urlopen(url)
    try:
        info = json.load(u)
        for i in info:
            if i['status'] == "attended":
                name = i['member']['name'].encode("utf-8").strip()

                """ Processes newbies """
                if name not in attended and name != 'Former member':
                    attended[name] = []     
                    g.add_vertex(name)
                    vid[name] = index
                    index += 1

                    """ Goes through the host list for this event
                        and draws an edge between each host and each
                        attendee
                        Updates list of newbies """
                    for h in event_host[uid]:
                        g.add_edge(vid[h], vid[name])
                        new = list(attended[h])
                        new.append(name)
                        attended[h] = new

                if name in events_per_member:
                    events_per_member[name] = events_per_member[name] + 1
                else:
                    events_per_member[name] = 1

    except ValueError:
        print "ValueError for " + url + " !"

    return index

"""
Input:  none
Output: none

Function also:  gets event_id with member_name
                makes vertices for hosts who have never attended an event prior to hosting
                tracks members who have been to more than one event
"""
def get_all_events():
    "Gets all the event id's in LetsHang along with its host"

    index = 0
    all_events_url = ("https://api.meetup.com/2/events?&photo-host=public"
                     "&group_urlname=20LetsHang&fields=event_hosts," 
                     "id&status=past" + keysign)
    info = json.load(urllib.urlopen(all_events_url))

    """ Parsing through each event """
    for i in info['results']:

        global total_events 
        total_events += 1
        event_id = i['id']

        if "event_hosts" in i:

            """ Parsing through each event host for specific event """
            for h in i['event_hosts']:

                member_name = h['member_name'].encode().strip()

                """ Updates event_host dict with name of member who hosted 
                    event with event_id """
                if event_id not in event_host:
                    event_host[event_id] = [member_name]
                else:
                    new = list([event_host[event_id]])
                    new.append(member_name)
                    event_host[event_id] = new

                """ Checking just in case member hosted event without attending
                    one before; need to start new vertex in graph """
                if member_name not in attended:
                    g.add_vertex(member_name)
                    vid[member_name] = index
                    index += 1
                    attended[member_name] = []
                else:
                    if member_name not in morethanone:
                        morethanone.append(member_name)

                index = get_attendance_for_event(event_id, index)
        
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
    dictlist = re.sub("\', \[\'", ": ", str(dictlist))
    dictlist = re.sub("\', \[\]\], \[\'", "\n", str(dictlist))
    dictlist = re.sub("\'\]\], \[\'", "\n", str(dictlist))
    dictlist = re.sub("\', \'", ", ", str(dictlist))
    dictlist = re.sub("\', \[\]\]\]", "", str(dictlist))
    dictlist = re.sub("\[\[\'", "", str(dictlist))
    f = open("/Users/andreawu/Documents/meetupnewbies/members.txt", "w")
    f.write("Total number of distinct attendees: " + str(len(vid.keys())) + "\n")
    f.write("Total number of events: " + str(total_events) + "\n\n")
    f.write("Total number of distinct attendees who have been to more than 1 event: " \
        + str(len(morethanone)) + "\n")
    morethanone_str = re.sub("\'", "\'", str(morethanone) + "\n")
    morethanone_str = re.sub("\'", "", morethanone_str)
    morethanone_str = re.sub("\[", "", morethanone_str)
    morethanone_str = re.sub("\]", "", morethanone_str)
    f.write("Attendees who have been to more than 1 event: " + morethanone_str)
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
