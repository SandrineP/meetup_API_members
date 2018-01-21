# meetup_API_members

With the other organisers of the AI club for Gender Minorities, we decided not to allow our members to be put directly on the main list as we wanted to prioritise those who are assiduous. So far, I've done that manually. I'm now trying to automate the process to gain time and to avoid human bias by giving a weight to the different situations (attended, no show, last day drop out, last minute excuse, waitlisted). There are things to improve and others that will come later (see comments).

The other thing I'll like to automate is the update of the database I use to register the attendance. The problem I have is that the meetup API allows only 200 requests per hour. The temporary solution that I found is to only add those who joined the waitlist.
