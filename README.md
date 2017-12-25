# HomebaseScraper

The end goal of this program is being able to collect information about work hours of employees
from Homebase (possibly including things like tip information too which would have to be entered manually)
and email them to an accountant for tax purposes. This is normally easy to do by utilizing the
Homebase API but it requires an additional monthly payment to Homebase which can be a large expense
for small restaurant owners.


Currently WIP

# Modules Used:
* PyQt for GUI
* SMTP for optional email service


# TODO:
- [ ] Add Linux and Mac support
- [ ] Check chrome and chromedriver version and update it during runtime without crashing
- [ ] Get user data about login and employee name information from a separate file
- [x] Add an email option using SMTP to send final data of employees
- [ ] Allow users to confirm the email that's being generate before it's sent
- [ ] Add a separate page or way to enter information about tips



# TODO Optional:
- [x] Add a gui element to make use easier
