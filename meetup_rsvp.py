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
weight_N = 0.8
weight_L = 0.2
weight_E = 0.1
weight_W = 0.4

# capacity of the event
capacity = int(input("Capacity of the event: "))

def to_main_list(event):

    if event['waitlist_count'] != 0:
        nb_ml = event['yes_rsvp_count']  # number of people already on the main list

        rsvps = client.GetRsvps(event_id = event['id'])     # getting the rsvp
                   # to do: get the waitlist only
                   # to do: ordering by date of answer

        if nb_ml < capacity:
            for m in rsvps.results:
                m_id = m['member']['member_id']
                    # to do: checking if question is answered

                if m_id not in members.index:
                    print(m_id, m['member']['name'])
                    client.CreateRsvp(event_id = event['id'],
                                      member_id = m_id,
                                      rsvp = 'yes')         # moving the member to the mainlist

                    members.loc[m_id] = m['member']['name']      #adding the new member to the database
                    members.loc[m_id, 1:6] = 0
                    members.loc[m_id, 6:] = 'NaN'


                else:
                    if members.loc[m_id, 'N - Nb No Show']
                     + members.loc[m_id, 'D - Nb last day drop out']
                     + members.loc[m_id, 'E - Nb last min excuse'] == 0:
                        client.CreateRsvp(event_id = event['id'],
                                          member_id = m_id,
                                          rsvp = 'yes')         # moving the member to the mainlist

                    else:
                        score = (weight_A*members.loc[m_id, 'A - Nb attended']
                                + weight_W*members.loc[m_id, 'W - Nb time wailtlisted'])
                                / max((weight_N*members.loc[m_id, 'N - Nb No Show']
                                + weight_D*members.loc[m_id, 'D - Nb last day drop out']
                                + weight_E*members.loc[m_id, 'E - Nb last min excuse']), 1)

                        if score > 1:
                            client.CreateRsvp(event_id = event['id'],
                                              member_id = m_id,
                                              rsvp = 'yes')         # moving the member to the mainlist

    # to do: complete the mainlist 24h before the event, whatever the score is

events = client.GetEvents(group_urlname = 'ai-club')

for event in events.results:
    to_main_list(event)

    # to do: fill the database with A/N/D/E/W

# saving the updated database
members.to_csv('AI_club_attendance.csv')    
