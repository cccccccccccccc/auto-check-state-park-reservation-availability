import datetime
import requests
import time
import logging
import smtplib
from email.header import Header
from email.mime.text import MIMEText
ENDPOINTS = 'https://washington.goingtocamp.com/api/availability/resourcedailyavailability'
WISHDATE = [
    
    ['2021-05-28','2021-05-29'],
]
# resourceid, bookingCid, mapid
WISHPOINT = {
    'Bayview C5':(-2147482823,1,-2147483330),    
}
CAMP_DETAILS_BY_LOCATIONID = {}

#send get request to website use javascript to get daily available information
def get_json(endpoint, params=None):
    return requests.get(ENDPOINTS, params=params, timeout=2).json()

def get_availabledate(resourceid,bookingCid,mapId):
    #get response from website resource is a list include availability day between target time range for the wishpark 
    resource = get_json(ENDPOINTS, {'resourceId':resourceid,'bookingCategoryId':bookingCid,'startDate':'2021-05-01T07:00:00.000Z','endDate':'2021-09-30T07:00:00.000Z'})
    availabledate = set()
    startdate = datetime.date(2021,5,1)
    # result is a str use to send email message to booking user
    result = ""
    for v in resource:
        if v['availability'] == 0:
            # logging.info(startdate)
            availabledate.add(startdate.strftime("%Y-%m-%d"))
        startdate+=datetime.timedelta(days=1)
    for wd in WISHDATE:
        #check if wishdate in the availabledate list
        if wd[0] in availabledate and wd[1] in availabledate:
            logging.info("find one")
            result+="There are two days available in wish:"+wd[0]+' '+wd[1]+'\n'
            result+=(get_reservation_link(mapId, bookingCid, wd[0], (datetime.datetime.fromisoformat(wd[1])+datetime.timedelta(days=1)).strftime("%Y-%m-%d"))+'\n')
    return result

def send_resulttoemail(result):
    # name, addr = parseaddr(s)
    # return formataddr((Header(name, 'utf-8').encode(), addr))
    logging.info("IN Send Step")
    from_addr = "xxx@gmail.com"
    password = "xxxxxx"
    to_addr = ["user1@gmail.com","user2@gmail.com"]
    smtp_server = "smtp.gmail.com"

    msg = MIMEText(result, 'plain', 'utf-8')
    #msg['From'] = from_addr
    #msg['To'] = to_addr
    msg['Subject'] = Header('Available cabin in wish', 'utf-8').encode()

    server = smtplib.SMTP_SSL(smtp_server, 465)
    server.set_debuglevel(1)
    server.ehlo()
    #server.starttls()
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()
    return

def get_WAPARKCABIN():
    """
    """
    result = ""
    for key in WISHPOINT.keys():
        logging.info(key)
        tmp = get_availabledate(WISHPOINT[key][0],WISHPOINT[key][1], WISHPOINT[key][2])
        if tmp!= "":
            result+= "After searching "+key+ " the result are in the below \n"+tmp
        time.sleep(2)
    logging.info(result)
    if result != "":
        data = ""
        with open('compare.txt','r') as f:
            data = f.read()
        if data == result:
            logging.info("Data is the same.")
        else:
            with open('compare.txt','w')as f: 
                f.write(result)  
            send_resulttoemail(result)
    return

def get_reservation_link(map_id, booking_Category_Id, start_date, end_date):
    
    return\
        'https://washington.goingtocamp.com/create-booking/results?mapId=%s&bookingCategoryId=%s&startDate=%s&endDate=%s&isReserving=true&partySize=3&nights=2'\
        %(map_id, booking_Category_Id, start_date, end_date)

if __name__ == '__main__':

    datestr = datetime.date.today().strftime("%Y-%m-%d")
    logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("log/"+datestr+".log"),
        logging.StreamHandler()
    ]
    )
    logging.info("================Start================")
    try:
        get_WAPARKCABIN()
    except:
        logging.exception("error")
    logging.info("================Finish================")