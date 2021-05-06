from app import mail, Message, app
import pickle

objects = pickle.load(open("pickleobjs", "rb"))
email = "psangita492@gmail.com"
obj = objects[email]
obj.pin = 370205
print(obj.__dict__)
print(obj.url)
print(email,obj)
slots = obj.get_available_slots()
formatted = ""
for each in slots:
    formatted = "\n" + formatted + each + "\n"
    formatted+=str(slots[each])+"\n"

print(formatted)