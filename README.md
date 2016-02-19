Meetup.com is a site where people make interest groups and organize events for groups, and people who join the groups attend the events. <br>

The data is for a Meetup group called 20LetsHang, where the common interest is meeting people in their 20's and joining fun activities around the South Bay Area of Northern California. The aggregated data in data.csv shows for each person in the group: the number of events s/he has attended and hosted, as well as the number and names of newbies (first timers to a 20LetsHang event) who attended for an event s/he hosted. <br>

graph.png shows the growth of the group using newbies. Each vertex represents a unique person who has attended a 20LetsHang event, and each edge represents a host-newbie relationship. For example, if Person A attended a 20LetsHang event for the first time hosted by Person B, Person B would be connected to Person A, and in data.csv, Person A would be on Person B's list of newbies. It is possible to be disconnected if a member hosts an event before attending an event. <br>

Technoligies used: Meetup API to grab the data, igraph to create the underlying graph, Cairo to draw a graph showing the connections, all written in Python.

To run, install Python igraph and pycairo, then run "python lh.py" in the command line.


