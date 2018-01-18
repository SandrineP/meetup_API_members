import meetup.api
import config
import pandas as pd

# Importing the members database
members = pd.read_csv('AI_club_attendance.csv')

client = meetup.api.Client()
client.api_key = config.MEETUP_KEY

# getting the list of members on the meetup website
meetup_list = client.GetMembers(group_urlname = 'ai-club')

# updating the database of members
for m in meetup_list.results:
    id = m['id']
    if id not in members.index:
        print(id, m['name'])
        members.loc[id] = m['name']
        members.loc[id, 1:6] = 0    # filling A, N, L, E and W (cf bellow) with zeros
        members.loc[id, 6:] = 'NaN'    # filling the rest of the row with NaN

# A = Attended
# N = No show
# L = Last day cancellation
# E = Last minute excuse
# W = Waitlisted

# saving the updated database
members.to_csv('AI_club_attendance.csv')
