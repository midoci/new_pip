#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import json
import hashlib
from _models.models import *
from django.shortcuts import redirect
import urllib
import random
import time
import string
import memcache

mc =memcache.Client(['127.0.0.1:12333'],debug=0)

APPID = 'wxf9e55c6e558ffd77'
SECRET = "9086dc2e2e95a72cee3f48181ee9a4ce"

class weixin(object):
    def __init__(self):
        pass
    
    def get_user_info(self,request,key = None):
	fr_id = request.GET.get('fr_id','')
	if not key:
	   key = 'index'
        url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=%s#wechat_redirect'
        if fr_id:
	    reurl = "http://hudong.midoci.com/dafuweng?fr_id=%s&" % fr_id
	    url = url % (APPID, reurl, key)
        else:
	    print url
	    url = url % (APPID, "http://hudong.midoci.com/dafuweng",key)
	return redirect(url)
   


 
    def dafuweng(self,request):
	code = request.GET.get('code')
	jsapi_ticket = self.get_jsapi_ticket(request,APPID, SECRET)  # ½ӿÚî 
	self_url = 'http://hudong.midoci.com'+request.get_full_path()
	sign = Sign(jsapi_ticket, self_url).sign()
	if code:
	    user_info = self.getUnionID(appid=APPID, secret=SECRET, code=code)
	    open_id = user_info.get('openid')
	    try:
		user_name = user_info.get('nickname','')
                user_img = user_info.get('headimgurl','')                
                open_id = user_info.get('openid')
                if FansUser.objects.filter(openid = open_id).exists():
                    pass
                else:
		    try:
                    	fansUserInfo = FansUser.objects.create(
                                           openid = open_id,
                                           user_name = user_name,
                                           fans_num = 0,
					   state = 1,
					   unique_id = user_info.get('unionid',''),
                                           user_img = user_img
                                           )
                    	fansUserInfo.save()
		    except Exception,e:
			print e
            except Exception,e:
                print e
	    u_id =  FansUser.objects.filter(openid = open_id)[0].u_id
	    fr_id = request.GET.get('fr_id','')
            if fr_id:
                fr_id = FansUser.objects.filter(openid = fr_id)[0].u_id
                self.save_friend(fr_id,u_id)
	    return u_id,sign,APPID,open_id,user_name,user_img
        else:
	    print 'error code'      

    



    
    def save_friend(self,fr_id,u_id):
        friend_info = FansUserFriends.objects.filter(u_id = u_id)
        if friend_info.exists():
	    o_id_list = friend_info[0].o_id
	    int_o_id_list = [int(i) for i in o_id_list.split(',')]
	    if int(fr_id) not in int_o_id_list:
		
	        o_id_list = str(o_id_list)+','+str(fr_id)
                friend_info.update(o_id = o_id_list
                                   )
        else:
            FansUserFriends.objects.create(u_id = u_id,
                                           o_id = fr_id
                                           )
        o_info = FansUserFriends.objects.filter(u_id = fr_id)
        if o_info.exists():
	    fo_id_list = o_info[0].o_id
	    int_fo_id_list = [int(i) for i in fo_id_list.split(',')]
	    if int(u_id) not in int_fo_id_list:
                fo_id_list = str(fo_id_list)+','+str(u_id)
                o_info.update(o_id = fo_id_list
                              )
        else:
            FansUserFriends.objects.create(u_id = fr_id,
                                           o_id = u_id
                                           )





    def get_jsapi_ticket(self,request,appid, secret):
	if not mc.get("ticket_%s"%appid):
            token = self.get_access_token(request,appid, secret)
            url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' % token
            response = urllib.urlopen(url)
            result = response.read().decode("utf8")
            response.close()
            result_dict = json.loads(result)
            mc.set("ticket_%s" % appid, result_dict['ticket'], 7000)
	    return result_dict['ticket']
        else:
	    return mc.get("ticket_%s" % appid)		

    def get_access_token(self,request,appid, secret):
	if not mc.get("ticket_%s"%appid):
            url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
                appid, secret)
            response = urllib.urlopen(url)
            result = response.read().decode("utf8")
            response.close()
            result_dict = json.loads(result)
            mc.set("token_%s" % appid, result_dict['access_token'], 7000)
            return result_dict['access_token']
        else:
	    return mc.get("token_%s" % appid)


	

    def getUnionID(self,appid=None, secret=None, code=None):
        userinfo = {}
        try:
            url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&redirect_uri&secret=%s&code=%s&grant_type=authorization_code'
            url = url % (appid, secret, code)
            response = urllib.urlopen(url)
            result = response.read().decode("utf8")
            response.close()
            result_dict = json.loads(result)
            userinfo_url = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s'
            userinfo_url = userinfo_url % (result_dict["access_token"], result_dict['openid'])
            response = urllib.urlopen(userinfo_url)
            userinfo = response.read().decode("utf8")
            userinfo = json.loads(userinfo)
            response.close()
            return userinfo
        except Exception, e:
	    print e
            return {}

        
    def summer_user_info(self,request):
        u_id = request.POST.get('u_id')
        u_id = json.loads(u_id)
        if SummerUserInfo.objects.filter(u_id = u_id).exists():
            s_user_info = SummerUserInfo.objects.filter(u_id = u_id)
            now_position = s_user_info[0].now_position
            coin = s_user_info[0].coin
            s_user_info.update(last_play_time = datetime.datetime.now())
	else:
            try:
                user_info = SummerUserInfo.objects.create(u_id = u_id,
                                                          coin = 10,
                                                          now_position = 0,
                                                          last_play_time = datetime.datetime.now(),
							  
							   )
                user_info.save()
                now_position = 0
                coin = 10
            except Exception,e:
                print e 
        return now_position,coin


    def shai(self,request):
        u_id = request.POST.get('u_id')
        u_id = json.loads(u_id)
        s_userinfo = SummerUserInfo.objects.filter(u_id = u_id) #objects
        shaizi_list = [1,2,3,4,5,6]
        step = random.choice(shaizi_list)
        now_position = s_userinfo[0].now_position
	collate_coin = s_userinfo[0].coin
        if collate_coin < 3:
            msg = 2
	    after_coin = collate_coin
            return msg,step,after_coin,collate_coin
        else:
            msg = 1
	    after_coin = int(collate_coin) -3
	    try:
	    	coin = int(collate_coin) - 3 + int(step)
            	now_position = (int(now_position)+int(step))%107
		s_userinfo.update(
                              now_position = str(now_position),
                              coin = coin,
                              last_play_time = datetime.datetime.now(),
                              )
	    except Exception,e:
		print e
            return msg,step,after_coin,collate_coin


class Sign:
    def __init__(self, jsapi_ticket, url):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])#ret Ê¸öäsorted(×µä«×µäkeyÅÐ ±älist
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        return self.ret



class summerManage(object):
    def __init__(self):
        pass

    def world_ranking(self):
        world_info = SummerUserInfo.objects.all().order_by('-coin')
        world_rank = []
        for i in world_info:
            world_rank.append({'head_img':FansUser.objects.get(u_id = i.u_id).user_img,
                               'user_name':FansUser.objects.get(u_id = i.u_id).user_name,
                               'coin':i.coin,}
                              )
	return world_rank
    

    def friend_ranking(self,request):
        u_id = request.POST.get('u_id')
        u_id = json.loads(u_id)
	o_id_list_info = FansUserFriends.objects.filter(u_id = u_id)
        o_id_list = []
        if o_id_list_info.exists():
            for i in o_id_list_info[0].o_id.split(','):
                o_id_list.append(int(i))
        o_id_list.append(int(u_id))
        friend_info = SummerUserInfo.objects.filter(u_id__in = o_id_list).order_by('-coin')
        friend_rank = []
	in_summerUserInfo_list = []
	for i in friend_info:
            fans_user_info = FansUser.objects.filter(u_id = int(i.u_id))
            if fans_user_info.exists():
                friend_rank.append(
                               {'head_img':fans_user_info[0].user_img,
                               'user_name':fans_user_info[0].user_name,
                               'coin':i.coin}
                                 )
	    in_summerUserInfo_list.append(int(i.u_id))
	not_in_summerUserInfo_list = list(set(o_id_list).difference(set(in_summerUserInfo_list)))
	not_in_rank = []
	for not_in in not_in_summerUserInfo_list:
	    fans_user = FansUser.objects.filter(u_id = int(not_in))
	    not_in_rank.append({
				'user_name':fans_user[0].user_name,
				'head_img':fans_user[0].user_img,
				})
	return friend_rank,not_in_rank
