import telebot
from telebot import types
import logging  
import datetime
import re
#import regex
import mysql.connector
import os
os.environ['HTTP_PROXY'] = 'http://kpproxygsit:8080'
os.environ['HTTPS_PROXY'] = 'http://kpproxygsit:8080'

def connect():
    mydb = mysql.connector.connect(
        host="10.43.3.226",
        port="3324",
        user="branchnet",
        password="devbranchnet",
        database="H2HRio"
    )
    return mydb


# Aktifkan logging
#  logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
#  logging.info('Starting Bot..........')

api = '2093008760:AAFvFcv2HcS_VTf73wJplriBQCeRWoATXE4'
bot = telebot.TeleBot(api)

def logStatus(message, partner, result, provider):
    date = datetime.datetime.now()
    date = date.strftime('%x %X')
    tanggal=str(date)
    first_name_log = message.from_user.first_name
    last_name_log = message.from_user.last_name

    mydb = connect()
    mycursor = mydb.cursor()
    # make table
    # print('--masuk 4--------------------'+ tanggal)
    mycursor.execute('CREATE TABLE IF NOT EXISTS log(first_name VARCHAR(50), last_name VARCHAR(50), partner VARCHAR(50),date VARCHAR(50),provider VARCHAR(50), result VARCHAR(50))')
    query = "INSERT INTO log(first_name, last_name, partner, date, Status_SLA, provider) VALUES(%s,%s,%s,%s,%s,%s)"
    vals = (first_name_log, last_name_log,partner, tanggal, result, provider)
    mycursor.execute(query,vals)
    mydb.commit()

def logPing(message, partner, result, provider):
    date = datetime.datetime.now()
    date = date.strftime('%x %X')
    tanggal=str(date)
    first_name_log = message.from_user.first_name
    last_name_log = message.from_user.last_name

    mydb = connect()
    mycursor = mydb.cursor()
    # make table
    # print('--masuk 4--------------------'+ tanggal)
    mycursor.execute('CREATE TABLE IF NOT EXISTS log(first_name VARCHAR(50), last_name VARCHAR(50), partner VARCHAR(50),date VARCHAR(50),provider VARCHAR(50), Status_SLA VARCHAR(50), Status_Ping VARCHAR(50))')
    query = "INSERT INTO log(first_name, last_name, partner, date, Status_Ping, provider) VALUES(%s,%s,%s,%s,%s,%s)"
    vals = (first_name_log, last_name_log, partner, tanggal, result, provider)
    mycursor.execute(query,vals)
    mydb.commit()

@bot.message_handler(commands=['halo','start', 'mulai', 'hallo'])
def send_welcome(message):
    print(message)
    name = message.from_user.first_name
    last_name = message.from_user.last_name
    bot.reply_to(message, 'Selamat Datang {} {}!!! \n 1. Ketikan /status Untuk Pengecekan Status SLA \n 2. Ketikkan /ping Untuk Melakukan Ping \n 3. Ketikkan /help Untuk menghubungi tim H2H BCA'.format(name,last_name))

@bot.message_handler(commands=['status'])
def check_status(message):
    bot.reply_to(message,"Silahkan ketikkan teks dengan format partner spasi nama perusahaan yang anda ingin cek status SLA'nya' seperti contoh berikut : \nstatus ABC")

@bot.message_handler(commands=['ping'])
def diy_problem(message):
    bot.reply_to(message,"Silahkan ketiklah teks dengan format ping spasi nama perusahaan yang anda ingin anda lakukan ping seperti contoh berikut : \nping ABC")

@bot.message_handler(commands=['help'])
def call_helpdesk(message):
    bot.reply_to(message,"Silahkan menghubungi salah satu dari brach team \nAlexander Patar : https://bit.ly/3Gfunvs\nMichael Sihombing : https://bit.ly/3naJ37u \nBaskoro Aditya Rahman: https://bit.ly/3nb5itZ \nAlexander Aryo Nugroho : https://bit.ly/32Y0zVM")

@bot.message_handler(regexp=r"(^status (.+))")
def reply_status(message):
    text = message.text
    regex = re.search(r'^status (.+)',text)
    partner = regex.group(1)
    mydb = connect()
    mycursor = mydb.cursor()
    query = "SELECT * FROM SLA where Partner='"+partner+"'" 
    mycursor.execute(query)  
    myresult = mycursor.fetchall()
    if(myresult):
        for i in myresult:
            bot.reply_to(message,'Partner : ' + i[1] + '\nProvider : ' + i[2] + '\nStatus SLA : ' + i[6] + '\n')
            provider = i[2]

            if(i[6]=='OK') :
                bot.reply_to(message,"Jika ingin mengecek status ping, silahkan ketikan teks dengan format ping spasi nama perusahaan yang anda ingin anda lakukan ping seperti contoh berikut : \nping ABC")
                result = i[6]
            else:   
                result = i[6]
                bot.reply_to(message, 'silahkan hubungi tim network terkait untuk mengatasi pemasalahan ini. ketikan /help untuk mendapatkan kontak tim')
            
            logStatus(message,partner,result,provider)
    else : 
        bot.reply_to(message,'Nama Partner tidak tersedia, silahkan memasukkan nama partner yang sesuai')

@bot.message_handler(regexp=r"(^ping (.+))")
def reply_status(message):
    text = message.text
    regex = re.search(r'^ping (.+)',text)
    partner = regex.group(1)
    mydb = connect()
    mycursor = mydb.cursor()
    query = "SELECT * FROM SLA where Partner='"+partner+"'" 
    mycursor.execute(query)  
    myresult = mycursor.fetchall()
    if(myresult):
        for i in myresult:
            bot.reply_to(message,'Partner : ' + i[1] + '\nProvider : ' + i[2] + '\nStatus ping : ' + i[5])
            provider = i[2]
            result = i[5]
            if(i[5]!='100/100') : 
                getPartner = "SELECT * FROM PIC_Provider where Provider='"+provider+"'"
                mycursor.execute(getPartner)
                myPartnerresult = mycursor.fetchall()
                if(myPartnerresult) :
                    for k in myPartnerresult:
                        bot.reply_to(message,'Status link sedang bermasalah, silahkan Hubungin pihak Provider terkait : \n' + k[1] + '    :   ' + k[2])
                    # a = 'Status link sedang bermasalah, silahkan Hubungin pihak Provider terkait : \n'
                    # for j in myPartnerresult:
                    #     print('aaaaaaaaaaaaaaaaaaaa')
                    #     b=j[1] + '   :   '+ j[2] + '\n'
                    #     b=bot.reply_to(j,'\n')
                    # bot.reply_to(message,a+b)
                
                # if(myPartnerresult):
                #     bot.reply_to(message,'Status link sedang bermasalah, silahkan Hubungin pihak Provider terkait : \n' + 
                       
                #     )
            logPing(message,partner,result,provider)
    else : 
        bot.reply_to(message,'Nama Partner tidak tersedia, silahkan memasukkan nama partner yang sesuai')

#kalo dia gak ngerti komennya
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Maaf saya tidak bisa mengerti apa maksud anda silahkan ketik /start untuk memulai")

print('Bot is running...')
bot.polling()