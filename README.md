# auto-check-state-park-reservation-availability
- Provide a way for users to configure preferred booking days and cabins sites.
- Implemente sending HTTP requests with Python, to get cabin availability information from the state park web server, get the response to analyze if there are wishing days in it.
- Schedule the program with launchctl, write logs to track running status.
- Send email to users using SMTP with booking information and link when new availability is found.


## Schedule this app
```
launchctl stop com.chen.statepark
launchctl list | grep com.chen
launchctl start com.chen.statepark
```