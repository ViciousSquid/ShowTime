# ShowTime

A useful tool for audio engineers/stage managers.
Time management for live performance slots. 

(or if you just need to monitor a timer over a LAN)

![image](https://github.com/ViciousSquid/ShowTime/assets/161540961/c0909c88-3526-4666-abe6-42440ffcb449)

No longer will you be asked the question "How much time do we have left?" or "Can we do an encore?" :-p

ShowTime will help guilt-trip your live performers into finishing ON TIME!

# Features
* Nice big fonts
* Set timers in 15 minute intervals
* Broadcasts over network - view the timer remotely from the mixing desk!!
* +15sec and +15min buttons
* When 5 minutes remain, timer turns yellow
* When time expires, counter turns red and starts counting up


* Supports up to four timers (named "Act one" to "act four")
* Names and default timers can be set using `config.json` in the `data` folder

## Usage

There is a **Windows EXE** in releases:
[https://github.com/ViciousSquid/ShowTime/releases]

Otherwise, Execute ShowTime.py with python (prerequisite of pygame 1.9.6+ is required)

![image](https://github.com/ViciousSquid/ShowTime/assets/161540961/ee8c41b8-c282-4c12-b866-5e643f775301) - to Start and stop the countdown

![image](https://github.com/ViciousSquid/ShowTime/assets/161540961/37bced85-cdf4-4a85-9a29-4d28c4f587d6) - to reset the countdown to the default (15 minutes)

![image](https://github.com/ViciousSquid/ShowTime/assets/161540961/c9c516cd-a5f0-4318-90ec-7161fa69562a) - to increase the timer by 15 minutes

![image](https://github.com/ViciousSquid/ShowTime/assets/161540961/fe53bc4f-3575-4fe6-8f10-d1906caf48a4) - to increase the timer by 15 seconds


--

NEW in version 1.03 is the ability to add multiple timers via JSON settings file (move through screens with < and > buttons)

Timer turns YELLOW when there are only 5 minutes remaining

Timer turns RED and continues counting up when time has expired

--


Clicking the small button in the top left labelled 'Remote' will start/stop a web server at localhost:8000 which will display the main timer

![image](https://github.com/ViciousSquid/ShowTime/assets/161540961/453289ea-edec-48a1-b6fa-597e818fd6e1)

Connect to [IP ADDRESS:8000] with a web browser to view the timer value


Error handling is not implemented yet:
If port 8000 is already in use for whatever reason, the app will crash.
