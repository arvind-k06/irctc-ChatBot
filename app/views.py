import json
import requests
import urllib.request
# from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse

@api_view(['POST'])
def train(request):
    if request.method == 'POST':
        api = 'l3l2o07acw'
        try:
            data = json.loads(request.body.decode('utf-8'))
            param = data['queryResult']['parameters']
            action = data['queryResult']['action']
            if action == 'trainbetweenstations':
                print(param)
                src = str(param['source'])
                dest = str(param['destination'])
                date = str(param['date'])
                date = date[8:10]+'-'+date[5:7]+'-'+date[:4]
                # print(src,dest,date)
                req = 'https://api.railwayapi.com/v2/between/source/' + src + '/dest/' + dest + '/date/' + date + '/apikey/'+ api +'/'
                print(req)
                r = requests.get(req)
                c = json.loads(r.content.decode("utf-8"))
                trains = (c["trains"])
                tes = ""
                for i in trains:
                    tes = tes + i['name'] + " and train number is " + i['number'] + ","

                s = {
                    "fulfillmentText" : "This is a sample response from your webhook!",
                    "fulfillmentMessages" :[{"text":{ "text": [tes]}}],"source" : ""}
                return JsonResponse(s, safe=False)
            elif action == 'livetrainstatus':
                print(param)
                num = str(int(param['number']))
                date = str(param['date'])
                date = date[8:10]+'-'+date[5:7]+'-'+date[:4]
                print(num,date)
                req = 'https://api.railwayapi.com/v2/live/train/' +num + '/date/' + date+'/apikey/'+ api + '/'
                print(req)
                r = requests.get(req)
                c = json.loads(r.content.decode("utf-8"))
                status = c['position']

                s = {
                    "fulfillmentText" : "This is a sample response from your webhook!",
                    "fulfillmentMessages" :[{"text":{ "text": [status]}}],"source" : ""}
                return JsonResponse(s, safe=False)
            elif action == 'pnr':
                print(param)
                num = str(int(param['number']))
                # print(num)
                req = 'https://api.railwayapi.com/v2/pnr-status/pnr/'+num+ '/apikey/'+ api + '/'
                print(req)
                r = requests.get(req)
                c = json.loads(r.content.decode("utf-8"))
                # print(c)
                pas = c['total_passengers']
                name = c['train']['name']

                temp = c['passengers']
                tes = ""
                for i in temp:
                    # print("passenger no" + str(i['no']) + "and the booking status is" + str(i['booking_status']))
                    tes = tes + "passenger no: "+ str(i['no']) + " and the booking status is " + str(i['booking_status']) + ", "
                tes = 'Ticket booked on '+ str(name) + ' for '+str(pas) +' members is as follows ,'+tes
                print(pas,name,tes)

                s = {
                    "fulfillmentText" : "This is a sample response from your webhook!",
                    "fulfillmentMessages" :[{"text":{ "text": [tes]}}],"source" : ""}
                return JsonResponse(s, safe=False)
            elif action == 'rescheduledtrains':
                print(param)
                date = str(param['date'])
                date = date[8:10]+'-'+date[5:7]+'-'+date[:4]
                req = 'https://api.railwayapi.com/v2/rescheduled/date/' + date+'/apikey/'+ api + '/'
                print(req)
                r = requests.get(req)
                c = json.loads(r.content.decode("utf-8"))
                trains = c['trains']
                # print(trains)
                tes = ""
                for i in trains:
                    # print(i['rescheduled_time'])
                    # print(i['name'], i['rescheduled_time'],i['rescheduled_date'])
                    tes=tes+"Train "+str(i['name'])+" rescheduled at "+str(i['rescheduled_time'])+" on "+str(i['rescheduled_date'])+", \n"
                s = {
                    "fulfillmentText" : "This is a sample response from your webhook!",
                    "fulfillmentMessages" :[{"text":{ "text": [tes]}}],"source" : ""}
                return JsonResponse(s, safe=False)
            elif action == 'seatavailability':
                print(param)
                date = str(param['date'])
                cls = str(param['class'])
                cls = cls[:2]
                print(cls)
                date = date[8:10]+'-'+date[5:7]+'-'+date[:4]
                req = 'https://api.railwayapi.com/v2/check-seat/train/'+str(param['number'])[:5]+'/source/' + str(param['source']) +'/dest/'+ str(param['destination']) +'/date/'+date+'/pref/'+ cls + '/quota/'+str(param['train_quota']) +'/apikey/'+ api + '/'
                print(req)
                r = requests.get(req)
                c = json.loads(r.content.decode("utf-8"))
                avail = c['availability'][0]
                print(avail['date'])
                print(c['train']['name'])
                tes = "Seat Availability status in " + str(c['train']['name']) +" on " + str(avail['date']) + " is " + str(avail['status'])+"."
                s = {
                    "fulfillmentText" : "This is a sample response from your webhook!",
                    "fulfillmentMessages" :[{"text":{ "text": [tes]}}],"source" : ""}
                return JsonResponse(s, safe=False)



            elif action == 'stationcodetoname':
                print(param)
                code = str(param['station_code'])
                req = 'https://api.railwayapi.com/v2/code-to-name/code/'+code+'/apikey/'+ api + '/'
                print(req)
                code_upper= code.upper()
                print(code_upper)
                r = requests.get(req)
                c = json.loads(r.content.decode("utf-8"))
                sta = c['stations']
                tes = ""
                # print(sta)
                for i in sta:
                    # print(i['code'] == code_upper)
                    if (i['code'] == code_upper):
                        tes = (i['name'])


                s = {
                    "fulfillmentText" : "This is a sample response from your webhook!",
                    "fulfillmentMessages" :[{"text":{ "text": [tes]}}],"source" : ""}
                return JsonResponse(s, safe=False)

            elif action == 'trainfareenquiry':
                print(param)
                date = str(param['date'])
                cls = str(param['class'])
                cls = cls[:2]
                print(cls)
                date = date[8:10]+'-'+date[5:7]+'-'+date[:4]
                req = 'https://api.railwayapi.com/v2/fare/train/'+str(param['number'])[:5]+'/source/'+str(param['source']) \
                      +'/dest/'+str(param['destination']) +'/age/'+str(param['age'])[:2]+'/pref/'+str(param['class']) \
                      +'/quota/'+str(param['train_quota']) +'/date/'+date+'/apikey/'+ api + '/'
                print(req)
                r = requests.get(req)
                c = json.loads(r.content.decode("utf-8"))
                tes = c['fare']
                s = {
                    "fulfillmentText" : "This is a sample response from your webhook!",
                    "fulfillmentMessages" :[{"text":{ "text": [tes]}}],"source" : ""}
                return JsonResponse(s, safe=False)



            elif action == 'trainname':
                print(param)
                # if (isinstance(param['number']))
                num = str(param['number'])[:5]
                req = 'https://api.railwayapi.com/v2/name-number/train/' + str(num) + '/apikey/' + api + '/'
                print(req)
                r = requests.get(req)
                c = json.loads(r.content.decode("utf-8"))
                tes = c['train']['name']
                s = {
                    "fulfillmentText" : "This is a sample response from your webhook!",
                    "fulfillmentMessages" :[{"text":{ "text": [tes]}}],"source" : ""}
                return JsonResponse(s, safe=False)

            elif action == 'trainroute':
                print(param)
                # if (isinstance(param['number']))
                num = str(param['number'])[:5]
                req = 'https://api.railwayapi.com/v2/route/train/'+num+ '/apikey/' + api + '/'
                print(req)
                r = requests.get(req)
                c = json.loads(r.content.decode("utf-8"))
                tes = ""
                route = c['route']
                # print(c['route'])
                for i in route:
                    # print(i)
                    tes = tes + str(i['station']['name']).title() +", "

                print(tes)

                s = {
                    "fulfillmentText" : "This is a sample response from your webhook!",
                    "fulfillmentMessages" :[{"text":{ "text": [tes]}}],"source" : ""}
                return JsonResponse(s, safe=False)

            elif action == 'cancelledtrain':
                print(param)
                date = str(param['date'])
                date = date[8:10]+'-'+date[5:7]+'-'+date[:4]
                num = str(param['number'])[:5]
                req = 'https://api.railwayapi.com/v2/cancelled/date/'+date +'/apikey/' + api + '/'
                print(req,num)
                r = requests.get(req)
                c = json.loads(r.content.decode("utf-8"))
                tes = ""
                trains = c['trains']
                tes = " Train numbered "+num+" is not cancelled"
                for i in trains:
                    if num == i['number']:
                        tes = "Yes, Train numbered "+num+" is Cancelled"
                print(tes)

                s = {
                    "fulfillmentText" : "This is a sample response from your webhook!",
                    "fulfillmentMessages" :[{"text":{ "text": [tes]}}],"source" : ""}
                return JsonResponse(s, safe=False)

        except Exception as err:
            return HttpResponse(err)