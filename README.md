Meetup.com is a site where people make interest groups and organize events for groups, and people who join the groups attend the events. <br>

I grabbed data for a Meetup group called 20LetsHang, where the common interest is meeting people in their 20's around South Bay Area of Northern California. The aggregated data shows the members who hosted events that newbies (first timers to a 20LetsHang event) attended. For example, if Person A attended a 20LetsHang event for the first time hosted by Person B, Person B would have Person A on Person B's list of newbies. <br>

I used the Meetup API to grab the data, igraph to create the underlying graph, and Cairo to draw a graph showing the connections. All this is written in Python.

To run, install Python igraph and pycairo, then run "python lh.py" in the command line.


