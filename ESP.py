import requests
import json
import os
from dotenv import load_dotenv
from datetime import date
import calendar

my_date = date.today()
WeekDayName = calendar.day_name[my_date.weekday()]

payload={}
headers = {'token': os.getenv('MAIN_KEY')} #Main Key
print(headers)
# headers = {'token': os.getenv('ADDITIONAL_KEY')} #Test Key

def Get_Status(payload, headers):
    url = "https://developer.sepush.co.za/business/2.0/status"
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)  

def Check_Allowance(payload, headers):
    url = "https://developer.sepush.co.za/business/2.0/api_allowance"

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

def Get_Area(payload, headers, search):
    url = "https://developer.sepush.co.za/business/2.0/areas_search?text=" + search

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

def main():
    
    # Get_Status(payload, headers)

    #Get_Area(payload, headers, "fluitjieskraal")

    Check_Allowance(payload, headers)
    
if __name__ == "__main__":
    main()

