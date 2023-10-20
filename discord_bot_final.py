import os
from dotenv import load_dotenv
import discord
import requests
import json
from datetime import date
import calendar
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='/', intents=intents)

my_date = date.today()
WeekDayName = calendar.day_name[my_date.weekday()]

payload={}
headers = {'token': os.getenv('MAIN_KEY')} #Main Key
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

def Stage_Switch(Stage):
    if Stage == "Stage 1":
        return "1"
    elif Stage == "Stage 2":    
        return "2"
    elif Stage == "Stage 3":
        return "3"
    elif Stage == "Stage 4":
        return "4"
    elif Stage == "Stage 5":
        return "5"
    elif Stage == "Stage 6":
        return "6"
    elif Stage == "Stage 7":
        return "7"
    elif Stage == "Stage 8":
        return "8"
    else:
        return "0"

def get_note_and_stages(payload, headers, area):
    
    url = "https://developer.sepush.co.za/business/2.0/area?id=" + area
    response = requests.post(url, headers=headers, data=payload, verify=False)
    requests.packages.urllib3.disable_warnings()
    data = response.json()

    if "events" not in data or not data["events"]:
        return "No loadshedding scheduled.", {}

    note = data["events"][0]["note"]

    response = requests.get(url, headers=headers, data=payload)

    if response.status_code == 200:
        data = response.json()

        note = data["events"][0]["note"]

        stages_by_day = {}
        for day in data["schedule"]["days"]:
            day_name = day["name"]
            stages = day["stages"]
            stages_by_day[day_name] = stages

        return note, stages_by_day
    else:
        print("Failed to retrieve data. Status code:", response.status_code)
        return None, None

def TodayLoadsheddingSchedule(note, stages_by_day):
    stage = int(Stage_Switch(note))
    print(stage)
    response = ""

    if note is not None and stages_by_day is not None:
        response += f"Note: {note}\n"
        for day, stages in stages_by_day.items():
            if day == WeekDayName:
                response += f"Stages for {day}: {stages[stage-1]}\n"

    return response

@bot.command()
async def durbanville(ctx):
    note, stages_by_day = get_note_and_stages(payload, headers, "capetown-6-durbanville")
    response = TodayLoadsheddingSchedule(note, stages_by_day)
    await ctx.send(response)

@bot.command()
async def muizenberg(ctx):
    note, stages_by_day = get_note_and_stages(payload, headers, "capetown-8-muizenberg")
    response = TodayLoadsheddingSchedule(note, stages_by_day)
    await ctx.send(response)

@bot.command()
async def kroonstad(ctx):
    note, stages_by_day = get_note_and_stages(payload, headers, "eskde-3-kroonstadindustriamoqhakafreestate")
    response = TodayLoadsheddingSchedule(note, stages_by_day)
    await ctx.send(response)

@bot.command()
async def potchefstroom(ctx):
    note, stages_by_day = get_note_and_stages(payload, headers, "eskme-5-potchefstroomjbmarksnorthwest")
    response = TodayLoadsheddingSchedule(note, stages_by_day)
    await ctx.send(response)

@bot.command()
async def orania(ctx):
    note, stages_by_day = get_note_and_stages(payload, headers, "eskde-1-fluitjieskraalthembelihlenortherncape")
    response = TodayLoadsheddingSchedule(note, stages_by_day)
    await ctx.send(response)

bot.run(os.getenv('DISCORD_TOKEN'))

