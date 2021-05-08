from app import mail, Message, app,data,get_dist_id
import pickle

#print(get_dist_id("Gujarat","Kutch"))
objects = pickle.load(open("pickleobjs", "rb"))
records = data.query.all()
groups = {}
for email in objects:
    obj = objects[email]
    if obj.data["by_district"] == 1:
        dist_id = get_dist_id(obj.data["state"],obj.data["district"])
        key = str(dist_id)+":"+str(obj.data["min_age"])
    else:
        key = str(obj.data["pin"]) + ":" + str(obj.data["min_age"])
    try:
        groups[key]["emails"].append(email)
    except:
        groups[key] = {"VaccineSlot_Object":obj,"emails":[email]}

for each in groups:
    print(each)
    print(groups[each])
    print()
#print(groups)
pickle.dump(groups,open("user_groups", "wb"))
# obj = pickle.load(open("user_groups", "rb"))
# print(obj)