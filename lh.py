import urllib, urllib2
import json
import sys

api_key = "7b4d4b32c605d5f4a7a6484a77231d"
keysign = "&key=" + api_key + "&sign=true"
auth_url = "https://secure.meetup.com/oauth2/authorize?client_id=l02bshoc9budf12krkgdvv42la&response_type=code&redirect_uri=http://localhost:8000/"
root_url = "https://api.meetup.com/20LetsHang/events/"
attendance_url = "/attendance?" + keysign

client_id = "l02bshoc9budf12krkgdvv42la"
client_sec = "g4uh4ls3ndloponstpcuej2v63"
redir = "http://localhost:8000/"
code = "1b8723bec6fc3cf6ba82786bc1108f47"

def authorize():
    req_url = "https://secure.meetup.com/oauth2/access"
    req_vals = { 'client_id' : client_id,
        'client_secret' : client_sec,
        'grant_type' : 'authorization_code',
        'redirect_uri' : redir,
        'code' : code }
    req_data = urllib.urlencode(req_vals)
    req = urllib2.Request(req_url, req_data)
    res = urllib2.urlopen(req)
    token = json.load(res).get('access_token')
    token_url = "https://secure.meetup.com/oauth2/authorize"
    token_vals = { 'client_id' : client_id,
        'response_type' : "token",
        'redirect_uri' : redir }
    token_data = urllib.urlencode(token_vals)
    print token_url + token_data
    u = urllib.urlopen(token_url + "?" + token_data)
    print u.read()

def get_attendance_for_event(id):
    "Gets the people who attended for given id meetup event"
    url = root_url + str(id) + attendance_url + keysign
    u = urllib.urlopen(url)

    info = json.load(u)
    attended = []
    for i in info:
        if i['status'] == "attended":
            attended.append(i['member']['name'])
    print attended

def get_all_events():
    "Gets all the event id's in LetsHang"
    all_events_url = "https://api.meetup.com/2/events?&photo-host=public&group_urlname=20LetsHang&fields=event_hosts,id&status=past" + keysign
    info = json.load(urllib.urlopen(all_events_url))
    event_host = dict() # maps event
    for i in info['results']:
        if "event_hosts" in i:
            for h in i['event_hosts']:
                event_host[i['id']] = h['member_id']
    for event in event_host:
        get_attendance_for_event(event)

if  __name__ == '__main__':
    # code = sys.argv[1]
    # get_attendance_for_event(220965394)
    get_all_events()
