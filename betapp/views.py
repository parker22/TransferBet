import operator
from itertools import groupby

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
import requests
from parsel import Selector
import httplib
import md5
import urllib
import random
import json
import schedule
import time
import re

from betapp.models import Player, Club, BetOdds
from betapp.serializers import BetOddsSerializer, ClubRumorsSerializer
from django.views.decorators.cache import cache_page

appid = '20170620000059559'
secretKey = 'VGfJwjHNDqF5BleTKMAK'
url = 'https://www.skybet.com/football/specials/transfer-specials'
httpClient = None
trans_api = '/api/trans/vip/translate'
fromLang = 'en'
toLang = 'zh'
salt = random.randint(32768, 65536)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def updateOdds(request):
    job()
    return HttpResponse("Odds Updated")


@cache_page(60 * 15)
def odds_detail(request):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        betodd = BetOdds.objects.order_by('-t_created')[0:1].get()
    except BetOdds.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = BetOddsSerializer(betodd)
        odds_json = json.dumps(betodd.odds)
        betodd.odds = translate_json(odds_json)
        return JsonResponse(serializer.data)


@cache_page(60 * 15)
def rumors_detail(request):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        betodd = BetOdds.objects.order_by('-t_created')[0:1].get()
    except BetOdds.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ClubRumorsSerializer(betodd)
        rumors_json = json.dumps(betodd.club_rumors)
        betodd.club_rumors = translate_json(rumors_json)
        return JsonResponse(serializer.data)


def job():
    text = requests.get(url).text
    print text
    selector = Selector(text=text)
    print len((selector.css('div.mktgrp > * >table')))
    print len((selector.css('div.mktgrp > * >h3')))
    player_odds_list = []
    club_odds = []
    for index, player in enumerate(selector.css('div.mktgrp > * >h3')):
        en_name = player.css('::text')[0].extract().encode('utf-8').strip()
        try:
            player = Player.objects.get(en_name=en_name)
        except Player.DoesNotExist:
            cn_name = translate(str(player.css('::text')[0].extract().encode('utf-8').strip()))
            player = Player(en_name=en_name, cn_name=cn_name)
            print 'new player' + str(en_name)
            player.save()
        print index
        clubs = selector.css('div.mktgrp > *>table')[index].css('td>a>span::text').extract()
        for club in clubs:
            club_en_name = club.encode('utf-8').strip()
            try:
                c = Club.objects.get(en_club_name=club_en_name)
            except Club.DoesNotExist:
                club_cn_name = translate(club_en_name)
                print 'new club' + str(club_en_name)
                c = Club(en_club_name=club_en_name, cn_club_name=club_cn_name)
                c.save()

        odds = selector.css('div.mktgrp > *>table')[index].css('td>a>b::text').extract()
        # print dict(zip(clubs, odds))
        # for player in selector.css('div.mktgrp >*>h3::text').extract():
        # 	print player.strip()
        player_odds = {'player': en_name, 'odds': [dict(zip(['club', 'odd'], row)) for row in zip(clubs, odds)]}
        player_odds_list.append(player_odds)
        items = [dict(zip(['club', 'odd', 'player'], row)) for row in
                 zip(clubs, odds, [en_name] * len(clubs))]
        club_odds += items
    keyfunc = operator.itemgetter("club")
    club_rumors_list = [{'club': key, 'rumors': list(grp)} for key, grp in groupby(sorted(club_odds, key=keyfunc),
                                                                                   key=keyfunc)]
    bo = BetOdds(odds=player_odds_list, club_rumors=club_rumors_list)
    bo.save()


def translate(q):
    sign = appid + q + str(salt) + secretKey
    m1 = md5.new()
    m1.update(sign)
    sign = m1.hexdigest()
    myurl = trans_api + '?appid=' + appid + '&q=' + urllib.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign

    try:
        httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()
        return json.loads(response.read())['trans_result'][0]['dst']

    except Exception, e:
        print e
    finally:
        if httpClient:
            httpClient.close()


def translate_json(json):
    d_c = dict(Club.objects.all().values_list('en_club_name', 'cn_club_name'))
    d_p = dict(Player.objects.all().values_list('en_name', 'cn_name'))

    d = d_c.copy()
    d.update(d_p)
    s = str(json)

    pattern = re.compile(r'\b(' + '|'.join(d.keys()) + r')\b')
    result = pattern.sub(lambda x: d[x.group()], s)
    return result