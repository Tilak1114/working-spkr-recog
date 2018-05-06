import smtplib

def sendotph(ead, epass, messg):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(ead, epass)

    msg = messg
    server.sendmail(ead, ead, msg)
    server.quit()