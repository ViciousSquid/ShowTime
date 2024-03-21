# ShowTime

A useful tool for audio engineers/stage managers.
Time management for live performance slots. 

![image](https://github.com/ViciousSquid/ShowTime/assets/161540961/c0909c88-3526-4666-abe6-42440ffcb449)

Put this on the stage.... No longer will you be asked the question "How much time do we have left?" or "Can we do an encore?" :-p

ShowTime will help guilt-trip your live performers into finishing ON TIME!

# Features
* Nice big fonts
* Set timers in 15 minute intervals
* Broadcasts over network - view the timer remotely from the mixing desk!!
* +15sec and +15min buttons
* When 5 minutes remain, timer turns yellow
* When time expires, counter turns red and starts counting up

## Usage

There is a **Windows EXE** in releases:
[https://github.com/ViciousSquid/ShowTime/releases]

Otherwise, Execute ShowTime.py with python (prerequisite of pygame 1.9.6+ is required)

Start/Stop - to Start and stop the countdown
Reset - to reset the countdown to the default (30 minutes)
+15sec/+15min - to increase the timer by that amount

Timer turns YELLOW when ther are only 5 minutes remaining
Timer turns RED and continues counting up when time has expired

Clicking the small button in the top left labelled 'Remote' will start a web server at localhost:8000

(This is currently very basic - Refreshing of the page is necessary to update the timer)


------------------

TO DO:  Split the master file into multiple python files for easier readability 
