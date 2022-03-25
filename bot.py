#from threading import Thread
import requests
from random import randint
from numpy import mean
from PIL import Image, ImageDraw, ImageFont
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram import Bot
import os

PORT = int(os.environ.get('PORT', 5000))
TOKEN="1849321051:AAERfOFiAI1IXQneI7gjHT6KNxE9eJuWHFE"

valves={'v1':{'x1':400,'y1':179,'x2':432,'y2':211,'color':"green"},
        'v2':{'x1':400,'y1':243,'x2':432,'y2':275,'color':"green"},
        'v3':{'x1':400,'y1':337,'x2':432,'y2':369,'color':"green"},
        'v4':{'x1':400,'y1':401,'x2':432,'y2':433,'color':"green"},
        'v5':{'x1':400,'y1':495,'x2':432,'y2':527,'color':"green"},
        'v6':{'x1':400,'y1':558,'x2':432,'y2':590,'color':"green"},
        }
flow_meters={'i1':{'x':695,'y':190},
            'i2':{'x':695,'y':238},
            'i3':{'x':695,'y':316},
            'i4':{'x':695,'y':363},
            'i5':{'x':695,'y':442},
            'i6':{'x':695,'y':490},
            'o1':{'x':1014,'y':190},
            'o2':{'x':1014,'y':238},
            'o3':{'x':1014,'y':316},
            'o4':{'x':1014,'y':363},
            'o5':{'x':1014,'y':442},
            'o6':{'x':1014,'y':490},
            }

farm={'b1':{'m1':'on','m2':'on','m3':'on','m4':'on','m5':'on','m6':'on','m7':'on','m8':'on','m9':'on','m10':'on','m11':'on','m12':'on','m13':'on','m14':'on','m15':'on','m16':'on','m17':'on','m18':'on','m19':'on','m20':'on','m21':'on','m22':'on','m23':'on','m24':'on','m25':'on',},
      'b2':{'m1':'on','m2':'on','m3':'on','m4':'on','m5':'on','m6':'on','m7':'on','m8':'on','m9':'on','m10':'on','m11':'on','m12':'on','m13':'on','m14':'on','m15':'on','m16':'on','m17':'on','m18':'on','m19':'on','m20':'on','m21':'on','m22':'on','m23':'on','m24':'on','m25':'on',},
      'b3':{'m1':'on','m2':'on','m3':'on','m4':'on','m5':'on','m6':'on','m7':'on','m8':'on','m9':'on','m10':'on','m11':'on','m12':'on','m13':'on','m14':'on','m15':'on','m16':'on','m17':'on','m18':'on','m19':'on','m20':'on','m21':'on','m22':'on','m23':'on','m24':'on','m25':'on',}
     }



# def telegram_bot_sendtext():
#     print("Write 'w_miner' to make bot send a miner warning\nWrite 'w_water' to make bot send a water loss warning\n" +\
#         "Write 'green' to make bot send an all green box status\nWrite 'otp' to make bot send an otp")
#     while True:
#         bot_message=input()
#         bot_token = TOKEN
#         #bot_chatID = '61700932'# mio chat id
#         bot_chatID = '-1001184533118'
#         if bot_message=='w_miner':
#             miner= "m" + str(randint(1,25))
#             box= "b" + str(randint(1,3))
#             farm[box][miner]='off'
#             text="⚠️ Miner " + miner + " in box " + box + " reached limit temperature, MINER STOPPED"
#             send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + text
#             response = requests.get(send_text)
#         elif bot_message=='w_water':
#             plate=randint(1,6)
#             valves["v"+str(plate)]['color']='red'
#             text="⚠️ Water loss detected in box " + str(randint(1,3)) + " plate " + str(plate) + " VALVE CLOSED"
#             send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + text
#             response = requests.get(send_text)
#         elif bot_message=='otp':
#             text="OctopusCooling - OTP CODE: "+str(randint(100000,999999)) + "\nFor level 2 auth insert this code"
#             send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + text
#             response = requests.get(send_text)

def extract_value(text):
    if len(text.split())>1:
        return text.split()[1].strip()
    else:
        return "Nanno"

def draw_plant():
    IMAGE_PATH="bitmap.png"
    OUTPUT_PATH="out.png"
    FONT = ImageFont.truetype("./Ubuntu-B.ttf", 18, encoding="unic")
    TEXT_COLOR=(0,0,255)

    image = Image.open(IMAGE_PATH)
    draw = ImageDraw.Draw(image)

    for valve in valves.keys():
        draw.ellipse((valves[valve]['x1'],valves[valve]['y1'],valves[valve]['x2'],valves[valve]['y2']),fill=valves[valve]['color'])

    for i in range(1,7):
        if valves["v"+str(i)]['color']=="green":
            text=str(randint(20,30))+" l/min"
            key_i="i"+str(i)
            key_o="o"+str(i)
            draw.text((flow_meters[key_i]['x'],flow_meters[key_i]['y']),text,TEXT_COLOR,font=FONT)
            draw.text((flow_meters[key_o]['x'],flow_meters[key_o]['y']),text,TEXT_COLOR,font=FONT)
        else:
            text="0 l/min"
            key_i="i"+str(i)
            key_o="o"+str(i)
            draw.text((flow_meters[key_i]['x'],flow_meters[key_i]['y']),text,(255,0,0),font=FONT)
            draw.text((flow_meters[key_o]['x'],flow_meters[key_o]['y']),text,(255,0,0),font=FONT)
    image.save(OUTPUT_PATH)


def farm_info(update, context):
    farm_name=extract_value(update.message.text)
    update.message.reply_text("Here some infos about " + farm_name + " farm:\n" +\
        "*Address:* Vicolo del Liceo, 1 - 38122 Trento (TN) \n*Box number:* 3\n*Miner number:* 75 \n*Status:* 🟢 Active" +\
        "\n*Average hashrate:* "+ str(randint(50000,60000))+ "\n*Active warnings:* 0",parse_mode=ParseMode.MARKDOWN)


def farm_status(update, context):
    farm_name=extract_value(update.message.text)
    update.message.reply_text("Here the status of the " + farm_name + " farm:\n"+\
        "   *Box 1 (3 miners):\n*" + \
        "       Miner 1: 🟢 Active\n" + \
        "       Miner 2: 🟡 Warnings\n" + \
        "       Miner 3: 🔴 Inactive",
        parse_mode=ParseMode.MARKDOWN)

def box_status(update, context):
    message_corpus=extract_value(update.message.text)
    splitted=message_corpus.strip().split(sep=".")
    if len(splitted)==2:
        box_name="b"+splitted[1]
        if box_name in farm.keys():
            msg_string="Farm *"+ splitted[0]+"*\nStatus of the box *" + box_name +"*:\n"
            for i in range(1,6):
                miner_string=""
                temp=[]
                for j in range(1,6):
                    temp_m=randint(80,90)
                    if farm[box_name]['m'+str(5*(i-1)+j)]=='on':
                        miner_string=miner_string+"    🟢 Miner: " + str(5*(i-1)+j) + \
                                                "\n           Status: " + farm[box_name]['m'+str(5*(i-1)+j)] + \
                                                "\n           Temperature: " + str(temp_m)  + "°" +\
                                                "\n           Hash rate: " + str(randint(50000,60000)) + \
                                                "\n           Operational time: " + str(randint(20,1440)) + "\n"
                    else:
                        miner_string=miner_string+"    🔴 Miner: " + str(5*(i-1)+j) + \
                                                "\n           Status: " + farm[box_name]['m'+str(5*(i-1)+j)] + \
                                                "\n           Temperature: 0°" + \
                                                "\n           Hash rate: 0"  \
                                                "\n           Operational time: 0\n"
                    temp.append(temp_m)
                
                floor_string=""
                f_temp= mean(temp)
                if f_temp<87:
                    floor_string="*Floor " + str(i) + " (temp: " + str(f_temp) + "°) *\n" + miner_string
                elif f_temp<89:
                    floor_string="*Floor " + str(i) + " (temp: " + str(f_temp) + "°) *\n" + miner_string
                else:
                    floor_string="*Floor " + str(i) + " (temp: " + str(f_temp) + "°) *\n" + miner_string
                msg_string=msg_string+floor_string+"\n" 
        else:
            msg_string="Box not found!"

        update.message.reply_text(msg_string,parse_mode=ParseMode.MARKDOWN)
    elif len(splitted)==0 or len(splitted)==1:
        box_name='b1'
        msg_string="Farm *Nanno*\nStatus of the box *b1*:\n"
        for i in range(1,6):
                miner_string=""
                temp=[]
                for j in range(1,6):
                    temp_m=randint(80,90)
                    if farm[box_name]['m'+str(5*(i-1)+j)]=='on':
                        miner_string=miner_string+"    🟢 Miner: " + str(5*(i-1)+j) + \
                                                "\n           Status: " + farm[box_name]['m'+str(5*(i-1)+j)] + \
                                                "\n           Temperature: " + str(temp_m)  + "°" +\
                                                "\n           Hash rate: " + str(randint(50000,60000)) + \
                                                "\n           Operational time: " + str(randint(20,1440)) + "\n"
                    else:
                        miner_string=miner_string+"    🔴 Miner: " + str(5*(i-1)+j) + \
                                                "\n           Status: " + farm[box_name]['m'+str(5*(i-1)+j)] + \
                                                "\n           Temperature: 0" + \
                                                "\n           Hash rate: 0" + \
                                                "\n           Operational time: 0\n"
                    temp.append(temp_m)
                
                floor_string=""
                f_temp= mean(temp)
                if f_temp<87:
                    floor_string="*Floor " + str(i) + " (temp: " + str(f_temp) + "°) *\n" + miner_string
                elif f_temp<89:
                    floor_string="*Floor " + str(i) + " (temp: " + str(f_temp) + "°) *\n" + miner_string
                else:
                    floor_string="*Floor " + str(i) + " (temp: " + str(f_temp) + "°) *\n" + miner_string
                msg_string=msg_string+floor_string+"\n" 
        update.message.reply_text(msg_string,parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("Incorrect box path format!",parse_mode=ParseMode.MARKDOWN)
    

def miner_status(update, context):
    message_corpus=extract_value(update.message.text)
    splitted=message_corpus.strip().split(sep=".")
    if len(splitted)==3:
        box="b"+str(splitted[1])
        if (box) in farm.keys():
            miner="m"+str(splitted[2])
            if miner in farm[box].keys():
                if farm[box][miner]=='on':
                    msg="Farm: *" + splitted[0] + "*\nBox number: *" + splitted[1] + "*\nMiner number: *" + splitted[2] + "*\nStatus: *" + farm[box][miner] + "*\nTemperature: " + str(randint(80,90)) + "°" + "\nHash rate: " + str(randint(50000,60000)) + "\nOperational time: " + str(randint(20,1440))
                else:
                    msg="Farm: *" + splitted[0] + "*\nBox number: *" + splitted[1] + "*\nMiner number: *" + splitted[2] + "*\nStatus: *off*\nTemperature: 0°\nHash rate: 0\nOperational time: 0"
            else:
                msg="Miner not found!"
        else:
            msg="Box not found!"
        update.message.reply_text(msg,parse_mode=ParseMode.MARKDOWN)
    elif len(splitted)==0 or len(splitted)==1:
        if farm['b1']['m1']=='on':
            msg="Farm: *Nanno*\nBox number: *1*\nMiner number: *1*\nStatus: *on*\nTemperature: " + str(randint(80,90)) + "°" + "\nHash rate: " + str(randint(50000,60000)) + "\nOperational time: " + str(randint(20,1440))
        else:
            msg="Farm: *Nanno*\nBox number: *1*\nMiner number: *1*\nStatus: *off*\nTemperature: 0°\nHash rate: 0\nOperational time: 0"
        update.message.reply_text(msg,parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("Incorrect miner path format!",parse_mode=ParseMode.MARKDOWN)

def start_miner(update, context):
    message_corpus=extract_value(update.message.text)
    splitted=message_corpus.strip().split(sep=".")
    if len(splitted)==3:
        if ("b"+str(splitted[1])) in farm.keys():
            if ("m"+str(splitted[2])) in farm["b"+str(splitted[1])].keys():
                if farm["b"+str(splitted[1])]["m"+str(splitted[2])]=='off':
                    farm["b"+str(splitted[1])]["m"+str(splitted[2])]='on'
                    msg="Farm: *" + splitted[0] + "*\nBox: *" + splitted[1] + "*\nMiner *" + splitted[2] + "*\n*STARTED*"
                else:
                    msg="Farm: *" + splitted[0] + "*\nBox: *" + splitted[1] + "*\nMiner *" + splitted[2] + "*\n*IS ALREADY ON*"
            else:
                msg="Miner not found!"
        else:
            msg="Box not found!"
        update.message.reply_text(msg,parse_mode=ParseMode.MARKDOWN)
    elif len(splitted)==0 or len(splitted)==1:
        if farm["b1"]["m1"]=='off':
            farm["b1"]["m1"]='on'
            msg="Farm: *Nanno*\nBox: *1*\nMiner *1*\n*STARTED*"
        else:
            msg="Farm: *Nanno*\nBox: *1*\nMiner *1*\n*IS ALREADY ON*"
        update.message.reply_text(msg,parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("Incorrect miner path format!",parse_mode=ParseMode.MARKDOWN)

def stop_miner(update, context):
    message_corpus=extract_value(update.message.text)
    splitted=message_corpus.strip().split(sep=".")
    if len(splitted)==3:
        if ("b"+str(splitted[1])) in farm.keys():
            if ("m"+str(splitted[2])) in farm["b"+str(splitted[1])].keys():
                if farm["b"+str(splitted[1])]["m"+str(splitted[2])]=='on':
                    farm["b"+str(splitted[1])]["m"+str(splitted[2])]='off'
                    msg="Farm: *" + splitted[0] + "*\nBox: *" + splitted[1] + "*\nMiner *" + splitted[2] + "*\n*STOPPED*"
                else:
                    msg="Farm: *" + splitted[0] + "*\nBox: *" + splitted[1] + "*\nMiner *" + splitted[2] + "*\n*IS ALREADY OFF*"
            else:
                msg="Miner not found!"
        else:
            msg="Box not found!"
        update.message.reply_text(msg,parse_mode=ParseMode.MARKDOWN)
    elif len(splitted)==0 or len(splitted)==1:
        if farm["b1"]["m1"]=='on':
            farm["b1"]["m1"]='off'
            msg="Farm: *Nanno*\nBox: *1*\nMiner *1*\n*STOPPED*"
        else:
            msg="Farm: *Nanno*\nBox: *1*\nMiner *1*\n*IS ALREADY OFF*"
        update.message.reply_text(msg,parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("Incorrect miner path format!",parse_mode=ParseMode.MARKDOWN)

def restart_miner(update, context):
    message_corpus=extract_value(update.message.text)
    splitted=message_corpus.strip().split(sep=".")
    if len(splitted)==3:
        if ("b"+str(splitted[1])) in farm.keys():
            if ("m"+str(splitted[2])) in farm["b"+str(splitted[1])].keys():
                    msg="Farm: *" + splitted[0] + "*\nBox: *" + splitted[1] + "*\nMiner *" + splitted[2] + "*\n*RESTARTED*"
            else:
                msg="Miner not found!"
        else:
            msg="Box not found!"
        update.message.reply_text(msg,parse_mode=ParseMode.MARKDOWN)
    elif len(splitted)==0 or len(splitted)==1:
        msg="Farm: *Nanno*\nBox: *1*\nMiner: *1*\n*RESTARTED*"
        update.message.reply_text(msg,parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("Incorrect miner path format!",parse_mode=ParseMode.MARKDOWN)

def plant_status(update, context):
    farm_name=extract_value(update.message.text)
    draw_plant()
    bot=Bot(token=TOKEN)
    bot.sendPhoto(chat_id=update['message']['chat']['id'],photo=open('out.png', 'rb'))

def open_valve(update, context):
    valve=extract_value(update.message.text)
    if valve in valves.keys():
        if valves[valve]['color']=="red":
            valves[valve]['color']="green"
            update.message.reply_text("Valve " + valve + " has been opened",parse_mode=ParseMode.MARKDOWN) 
        else:
            update.message.reply_text("Valve " + valve + " is already open",parse_mode=ParseMode.MARKDOWN) 
    else:
            update.message.reply_text("Invalid valve name!",parse_mode=ParseMode.MARKDOWN) 

def close_valve(update, context):
    valve=extract_value(update.message.text)
    if valve in valves.keys():
        if valves[valve]['color']=="green":
            valves[valve]['color']="red"
            update.message.reply_text("Valve " + valve + " has been closed",parse_mode=ParseMode.MARKDOWN) 
        else:
            update.message.reply_text("Valve " + valve + " is already closed",parse_mode=ParseMode.MARKDOWN) 
    else:
            update.message.reply_text("Invalid valve name!",parse_mode=ParseMode.MARKDOWN)  

def main():
    upd= Updater(TOKEN, use_context=True)
    disp=upd.dispatcher

    disp.add_handler(CommandHandler("farm_info", farm_info))
    #disp.add_handler(CommandHandler("farm_status", farm_status))
    disp.add_handler(CommandHandler("box_status", box_status))
    disp.add_handler(CommandHandler("miner_status", miner_status))
    disp.add_handler(CommandHandler("start_miner", start_miner))
    disp.add_handler(CommandHandler("stop_miner", stop_miner))
    disp.add_handler(CommandHandler("restart_miner", restart_miner))
    disp.add_handler(CommandHandler("plant_status", plant_status))
    disp.add_handler(CommandHandler("open_valve", open_valve))
    disp.add_handler(CommandHandler("close_valve", close_valve))

    upd.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    upd.bot.setWebhook('https://afternoon-escarpment-95244.herokuapp.com/' + TOKEN)

    upd.idle()


if __name__=='__main__':
    #listener = Thread(target=telegram_bot_sendtext)
    #listener.start() 
    main()

