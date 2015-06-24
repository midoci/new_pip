#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import urllib
from _models.models import *
from django.http import HttpResponse
from django.shortcuts import redirect
from utils.views import mp_render
import random
from models import weixin
from models import summerManage
#from utils.views import LazyEncoder
weiXin = weixin()
summerManage = summerManage()


def hello(request):
    return HttpResponse('hello')

def dafuweng(request):
    u_id,sign,appid,open_id,user_name,user_img = weiXin.dafuweng(request)
    data = {'u_id':u_id,'sign':sign,'appid':appid,"user_name":user_name,"user_img":user_img,'open_id':open_id}
    return mp_render(request, "index.html",data)


def summer(request):
    return weiXin.get_user_info(request)



def admin(request):
    return mp_render(request, "admin.html")

def getUserInfo(request):
    now_position,coin = weiXin.summer_user_info(request)
    return HttpResponse(json.dumps({"now_position": now_position,"coin":coin}))

def shai(request):
    msg,step,after_coin,collate_coin = weiXin.shai(request)
    return HttpResponse(json.dumps({"msg": msg,"step":step,"after_coin":after_coin,"collate_coin":collate_coin}))

def world_ranking(request):
    world_rank = summerManage.world_ranking()
    return HttpResponse(json.dumps({"world_rank":world_rank}))

def friend_ranking(request):
    friend_rank,not_in_rank = summerManage.friend_ranking(request)
    return HttpResponse(json.dumps({"friend_rank":friend_rank,"not_in_rank":not_in_rank}))



