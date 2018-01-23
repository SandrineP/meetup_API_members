import meetup.api
import config
import pandas as pd

# Importing the members database
members = pd.read_csv('AI_club_attendance.csv')

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

def to_main_list(event):
    capacity = int(event['description'][-7:-4])    # capacity of the event

    if event['waitlist_count'] != 0:
        nb_ml = event['yes_rsvp_count']    # number of people already on the main list

        rsvps = client.GetRsvps(event_id = event['id'])    # getting the rsvp
        w = [rsvps.results[i]['response'] == 'waitlist' for i in range(len(rsvps.results))]
        waitlist = [m for (m,r) in zip(rsvps.results, w) if r]
                   # to do: ordering by date of answer

        if nb_ml < capacity:
            for m in waitlist:
                m_id = m['member']['member_id']
                    # to do: checking if question is answered

                if m_id not in members.index:
                    print(m_id, m['member']['name'])
                    move_to_main_list(event['id'], m_id)    # moving the member to the mainlist

                    members.loc[m_id] = m['member']['name']    #adding the new member to database
                    members.loc[m_id, 1:6] = 0
                    members.loc[m_id, 6:] = 'NaN'


                else:
                    s = [w*p for w,p in zip(weight,members.loc[m_id][1:6])]
                    score = sum(s)

                    if score >= 0:
                        move_to_main_list(event['id'], m_id)    # moving the member to the mainlist

    # to do: complete the mainlist 24h before the event, whatever the score is

events = client.GetEvents(group_urlname = 'ai-club')

for event in events.results:
    to_main_list(event)

    # to do: fill the database with A/N/D/E/W

# saving the updated database
members.to_csv('AI_club_attendance.csv')
