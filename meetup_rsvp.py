import meetup.api
import config
import pandas as pd
from datetime import datetime

# Importing the members database
members = pd.read_csv('AI_club_attendance.csv', index_col='member ID')

client = meetup.api.Client()
client.api_key = config.MEETUP_KEY

# A = Attended
# N = No show
# L = Last day cancellation
# E = Last minute excuse
# W = Waitlisted

# weights
weight_A = 1
weight_N = -1
weight_L = -0.3
weight_E = -0.2
weight_W = 0.5


def move_to_main_list(ev_id, m_id):
    client.CreateRsvp(event_id = ev_id, member_id = m_id, rsvp = 'yes')


def decide_to_move(ev_id, m, n):
    m_id = m['member']['member_id']

    if m_id not in members.index:
        move_to_main_list(ev_id, m_id)    # moving the member to the mainlist
        n += 1    # updating the number of people on the main list

        members.loc[m_id] = m['member']['name']    #adding the new member to database
        members.loc[m_id, 1:6] = 0    # filling A, N, L, E and W (cf bellow) with zeros
        members.loc[m_id, 6:] = 'NaN'    # filling the rest of the row with NaN

    else:
        weight = [weight_A, weight_N, weight_L, weight_E, weight_W]
        s = [w*p for w,p in zip(weight,members.loc[m_id][1:6])]
        score = sum(s)

        if score >= 0:
            move_to_main_list(ev_id, m_id)    # moving the member to the mainlist
            n += 1    # updating the number of people on the main list


def to_main_list(event):
    capacity = int(event['description'][-7:-4])    # capacity of the event

    if event['waitlist_count'] != 0:
        nb_ml = event['yes_rsvp_count']    # number of people on the main list

        rsvps = client.GetRsvps(event_id = event['id'])    # getting the rsvp
        rsvps_w = [rsvps.results[i]['response'] == 'waitlist' for i in range(len(rsvps.results))]
        waitlist = [m for (m,r) in zip(rsvps.results, rsvps_w) if r]
        waitlist_ordered = sorted(waitlist, key=lambda item: item['mtime'])    # ordering the waitlist by time answered

        for m in waitlist_ordered:
            if nb_ml < capacity:

                if 'answers' in m.keys():
                    if len(m['answers'][0])>4:
                        decide_to_move(event['id'], m, nb_ml)

                else:
                    decide_to_move(event['id'], m, nb_ml)

    ### to do: complete the mainlist 24h before the event, whatever the score is

events = client.GetEvents(group_urlname = 'ai-club')

for event in events.results:
    to_main_list(event)

    ### to do: fill the database with A/N/D/E/W

# saving the updated database
members.to_csv('AI_club_attendance.csv')
