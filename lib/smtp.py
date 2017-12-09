from smtplib import SMTP

# we're probably going to have a dump of all emails generated and they will be
# saved in a folder with the date as the file name

# header information like recepients will be grabbed from a static text file
# that the user will eventually be able to edit on their own with a nice GUI

def send_email(email, password, recepient, recepient_name, body, date):
    """
    Parameters
    ----------
    email : account's email addr
    password : str || array of email addr
    recepient :  email addr of recepient
    recepient_name : str
    body : str
    date : array: { date[0] : month, date[1] : day, date[2] : year }

    """
    with SMTP('smtp.gmail.com:587') as smtp:
        # smtp.set_debuglevel(2)


        # for ensuring consistent behavior when setting
        # headers for multiple recepients
        if type(recepient) is not list:
            recepient = [recepient]
            print("Recepients converted to list")  # debug

        smtp.ehlo()
        smtp.starttls()
        login = smtp.login(email, password)

        # login[0] == status response, 235 is OK

        if login[0] == 235:
            print("Successfully logged in to {}\n".format(email))
        else:
            # catchall
            # TODO: catch for google's dumbass authorization thing
            return print(
            "There was a problem logging in\n" + \
            "Code: {}\nDescription: {}\n".format(login[0], login[1])
            )

        # setting headers
        _from = "From {}".format(email)

        # it's unlikely that the email will need to be sent to
        # more than one person at a time but if that's the case
        # then GUI input will need options for multiple recepients

        # converting the date to subject string
        _subject_str = "Olive Tree {} Payroll Details".format('/'.join(str(x) for x in date))

        #adding all to header
        _subject = "Subject: {}\n\n".format(_subject_str)

        # print(_subject)
        # not sure if _subject + body is the best way to do this

        # ---- sending the email ------
        try:
            smtp.sendmail(email, recepient, _subject + body)
        except Exception as e:
            print("An error occurred.")
            return print(e)


        print("Email sent successfully.")