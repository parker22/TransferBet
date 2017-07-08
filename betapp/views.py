# encoding: utf-8
import httplib
import json
import md5
import operator
import random
import re
import urllib
from itertools import groupby

import requests
# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page
from parsel import Selector

from betapp.models import Player, Club, BetOdds
from betapp.serializers import BetOddsSerializer, ClubRumorsSerializer

appid = '20170620000059559'
secretKey = 'VGfJwjHNDqF5BleTKMAK'
url = 'http://128.199.77.172:5000/'
httpClient = None
trans_api = '/api/trans/vip/translate'
fromLang = 'en'
toLang = 'zh'
salt = random.randint(32768, 65536)

<<<<<<< HEAD
club_name_dict={
    'To Stay at Manchester City':'To Stay at Man City',
    'To Stay at Manchester Utd':'To Stay at Man Utd',
'To Stay at Manchester United':'To Stay at Man Utd',
    'Manchester United':'Man Utd',
'Manchester Utd':'Man Utd',
'Manchester City':'Man City',
    'Borussia Dortmund':'Dortmund',
'C Palace':'Crystal Palace'
=======
club_name_dict = {
    'To Stay at Manchester City': 'To Stay at Man City',
    'To Stay at Manchester Utd': 'To Stay at Man Utd',
    'To Stay at Manchester United': 'To Stay at Man Utd',
    'Manchester United': 'Man Utd',
    'Manchester Utd': 'Man Utd',
    'Manchester City': 'Man City',
    'Borussia Dortmund': 'Dortmund',
    'C Palace': 'Crystal Palace',
>>>>>>> cc52fb99d726e46391656ecee1b372df3a077472
}


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def updateOdds(request):
    job()
    return HttpResponse("Odds Updated")


@cache_page(60 * 10)
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
        betodd.odds = odds_json
        return JsonResponse(serializer.data)


@cache_page(60 * 10)
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
        betodd.club_rumors = rumors_json

        return JsonResponse(serializer.data)


def player_detail(request):
    player_name = u'拉卡泽特'
    odds_list = BetOdds.objects.filter(odds__0__player=player_name).values_list()
    player_clubs_list = []
    if request.method == 'GET':
        for odds in odds_list:
            t_created = odds[1]
            odd = next((item['odds'] for item in odds[2] if item['player'] == player_name), None)
            player_clubs_list.append({'t_created': t_created, 'odd': odd})
        return JsonResponse({'player_clubs_list': player_clubs_list})


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
        cn_name = ''

        try:
            player = Player.objects.get(en_name=en_name)
            cn_name = player.cn_name
        except Player.DoesNotExist:
            cn_name = translate(str(player.css('::text')[0].extract().encode('utf-8').strip()))
            player = Player(en_name=en_name, cn_name=cn_name)
            print 'new player' + en_name
            player.save()
        clubs = selector.css('div.mktgrp > *>table')[index].css('td>a>span::text').extract()
        clubs = [
            str(club).replace("(Does not include returning on loan following a permanent deal elsewhere)", "").encode(
                'utf-8').strip() for club in clubs]
        clubs_cn = []
        for club in clubs:
            if club in club_name_dict:
                club = club_name_dict[club]
            club_en_name = club
            club_cn_name = ''
            try:
                c = Club.objects.get(en_club_name=club_en_name)
                club_cn_name = c.cn_club_name
            except Club.DoesNotExist:
                club_cn_name = translate(club_en_name)
                print 'new club' + club_en_name
                c = Club(en_club_name=club_en_name, cn_club_name=club_cn_name)
                c.save()
            clubs_cn.append(club_cn_name)

        odds = selector.css('div.mktgrp > *>table')[index].css('td>a>b::text').extract()
        # print dict(zip(clubs, odds))
        # for player in selector.css('div.mktgrp >*>h3::text').extract():
        # 	print player.strip()
        player_odds = {'player': cn_name, 'odds': [dict(zip(['club', 'odd'], row)) for row in zip(clubs_cn, odds)]}
        player_odds_list.append(player_odds)
        items = [dict(zip(['club', 'odd', 'player'], row)) for row in
                 zip(clubs_cn, odds, [cn_name] * len(clubs_cn))]
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
    s = json

    # for key, value in org.items():
    #     text = text.replace(key, value)
    pattern = re.compile(r'\b(' + '|'.join(d.keys()) + r')\b')
    result = pattern.sub(lambda x: d[x.group()].encode('utf-8'), s.encode('utf-8'))
    return result


job()
