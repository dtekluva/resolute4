from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from main.models import Customer, Location
import json
from itertools import chain #allow for merging multiple querysets frorm different models
from django.core import serializers
import math
import datetime
from snippet import helpers
from os import path
from django.views.decorators.csrf import csrf_exempt
# from rest_framework import serializers
# Create your views here.

host = "http://localhost:8000/"
print('<===RAN THIS FILE===>'.center(20))

@csrf_exempt
def main(request):
# Create your views here.    
    # print(request.body)
    if request.method == 'POST':    
        reqPOST = str(request.body)
        reqGET = str(json.loads(request.body))
        print(str(reqGET))
        print(request.POST.get('resource', ''))
        raw_time = str(datetime.datetime.now())
        clean_time = raw_time[:18]

    if path.exists("log.txt"):
        log = open('log.txt', 'a')
    else:
        log = open('log.txt', 'a')
        log.write('|-------TIME-------, -------POST-------, ------GET-------|\n')

    new_log = '{0},{1},{2}\n'.format(clean_time,reqPOST,reqGET)
    log.writelines(new_log )
    log.close()

    return HttpResponse(read_file())

def read_file():
    log = open('log.txt', 'r')
    raw_response = (log.read().split('\n'))
    # print(raw_response)
    response = ''
    for line in raw_response:
        response += '<div>'+ str(line.replace('<','\t')).replace('>','\t').replace(',', '  <===>  ') + '<div>'
    log.close()
    return response

    
@csrf_exempt
def end(request):

    
    if request.method == 'GET':
        post = (request.GET)
        target = Customer.objects.get(id = post["device"])
        target.lng = post['ln']
        target.lat = post['lt']
        target.address  = helpers.get_address(post['lt'],post['ln'])
        target.is_panicking = True
        target.panicked = datetime.datetime.now()
        target.save()

        new_location = Location.objects.create(lat = target.lat, lng = target.lng, address = target.address, customer_id = target.id,
                                                speed = post['sog'], accuracy = post['hdop'])

        return HttpResponse(json.dumps({'success':'success', "panic_status":target.is_panicking}))

        
    return HttpResponse('Unrecognisable request method, cannot understand')


def check(request, slug):

    customer = Customer.objects.get(slug = slug) #for filtering get just one customer 
    customers = Customer.objects.filter(slug = slug) # for iteration
    locations = serializers.serialize("json", list(chain(Location.objects.filter(customer_id = customer.id)[:40], customers)) )



    return HttpResponse(locations)



def track(request, slug):

    return render(request, 'quickbooks/tracking.html', {"slug":slug})

def test(request):

    return render(request, 'quickbooks/test.html')

def check_distance(old_coord, new_coord):

    a =  old_coord[0] - new_coord[0] #lat difference as opposite
    b =  old_coord[1] - new_coord[1] #lng difference as adjacent
    c = a **2 + b **2 #hypothenus as distance between two points

    c = math.sqrt(c)
    print(c)
    # 0.0009 = "100m"
    # 0.009 = "1km"
    if c >= 0.00001:
        return True
    
    else:
        return False

