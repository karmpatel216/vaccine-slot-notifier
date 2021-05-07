import pickle
from app import data
import time
from app import mail, Message, app

def format_slots(slots):
    formatted = ""
    for each in slots:
        formatted = "\n" + formatted + each + "\n"
        formatted += str(slots[each]) + "\n"
    return formatted
while True:
    rows = data.query.all()
    objects = pickle.load(open("pickleobjs", "rb"))
    for user in rows:
        email = user.email
        #print(f"user={email}")
        if objects[email]:
            obj = objects[email]
            slots = obj.get_available_slots()
            #print(slots)
            if slots != {}:
                with app.app_context():
                    msg = Message('Vaccine Slot is Available', sender=app.config['MAIL_USERNAME'], recipients=[email])
                    n_centers = len(slots)
                    if n_centers < 50:
                        formatted_slots = format_slots(slots)
                    else:
                        formatted_slots = str(slots)
                    #print(formatted_slots)
                    if user.by == "Area":
                        msg.body = "Dear user,\nFollowing slots are available in " + str(user.district) +"\nAge group:"+ str(user.min_age) +"\n" + str(formatted_slots)
                        print(f"vaccine is available in {user.district}")
                    else:
                        msg.body = "Dear user,\nFollowing slots are available in "+ str(user.pin) +"\nAge group:"+ str(user.min_age) +"\n" + str(formatted_slots)
                        print(f"vaccine is available in {user.pin}")
                    mail.send(msg)

                    #print(msg.body)
                    print(f"mail sent to-{email}")
        else:
            print("object not found")
    print("*********************************")
    time.sleep(600)