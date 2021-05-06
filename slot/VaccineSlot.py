import json
import urllib.request
import requests
import os
from datetime import datetime

class VaccineSlot:

    def __init__(self,data):
        self.data = data
        date = data["date"]
        if data["by_district"] == 1:

            with open("district_ids.json", "r") as fp:
                self.district_ids = json.load(fp)
            dist_id = self.district_ids[data["state"]][data["district"]]

            self.url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={dist_id}&date={date}"
        else:
            pin = data["pin"]
            self.url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pin}&date={date}"


    def get_available_slots(self):
	proxies = {
	 "http": "http://14.140.131.82:3128",
	 "https": "http://14.140.131.82:3128"
	}
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}
        #resp = eval(requests.get(self.url, proxies=urllib.request.getproxies()).text)
        #resp = eval(urllib.request.urlopen(self.url).read().decode('utf-8'))
        resp = eval(requests.get(self.url, headers=headers).content.decode('utf-8'),proxies=proxies)
        all_centers = resp['centers']
        min_age = self.data['min_age']
        print("age=",min_age)
        available = {}
        for each in all_centers:
            center_name = each["name"].strip()
            if each['sessions']:
                for sess in each['sessions']:
                    #print(sess)
                    if sess['min_age_limit'] == min_age and sess["available_capacity"] >= 1:
                        data = {"available_capacity": sess["available_capacity"]
                            , "date": sess["date"]}
                        if center_name not in available:
                            available[center_name] = [data]
                        else:
                            available[center_name].append(data)
                        #print("available!")
        return available


