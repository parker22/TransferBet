# encoding: utf-8

import httplib
import json
import md5
import random
import urllib

# Create your views here.
import requests
from fake_useragent import UserAgent
from parsel import Selector

ua = UserAgent()
print(ua.chrome)
header = {'User-Agent': str(ua.chrome)}
appid = '20170620000059559'
secretKey = 'VGfJwjHNDqF5BleTKMAK'
url = 'https://www.skybet.com/football/specials/transfer-specials'
httpClient = None
trans_api = '/api/trans/vip/translate'
fromLang = 'en'
toLang = 'zh'
salt = random.randint(32768, 65536)

club_name_dict = {
    'To Stay at Manchester City': 'To Stay at Man City',
    'To Stay at Manchester Utd': 'To Stay at Man Utd',
    'To Stay at Manchester United': 'To Stay at Man Utd',
    'Manchester United': 'Man Utd',
    'Manchester Utd': 'Man Utd',
    'Manchester City': 'Man City',
    'Borussia Dortmund': 'Dortmund'
}

header_info = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
}

import mechanize


def job():
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [("user-agent",
                      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"),
                     ('authority', 'www.skybet.com'),
                     ('method', 'GET'),
                     ('path', '/football/specials/transfer-specials'),
                     ('scheme', 'https'),
                     (
                         'accept',
                         'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'),
                     ('accept-encoding', 'gzip, deflate, br'),
                     ('accept-language', 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2'),
                     ('cache-control', 'max-age=0'),
                     ('cookie',
                      'sbgCFcustrandno01=82.2; sbgCAcid01=3EBFE797C814A6A4B6B182391BA5B43B; _ga=GA1.2.200552123.1496285371; betCEsessid01=3q9ad11ench0v48vqd6o2cvnf3; sbgCEsitevisitor=11; sbgCEsiteactiveBet=7b674d7ff7c810a5bad7b5f11999f7fd; sbgCAtrial01=betCOB,BetNGU,betTrial7,bingoappNativeNavBar,vegasappNativeNavBar; beta_site_stick=YmV0YQ==; sbgCEsiteactiveSSO=cc89f90083ecb66e2cfc2c50a43dc22d; config=%7B%22attemptedSSOLogin%22%3Atrue%7D; SSOSESSID=828d661bfc4a76371081e3fe508ef81f; __SBA_POLLTIME=1499223165446|loggedOut|true; SSO_SESS_ID=828d661bfc4a76371081e3fe508ef81f; betSsoAutoLoginAttempted=1499223668675; s_pers=%20s_vnum%3D1501814810661%2526vn%253D1%7C1501814810661%3B%20s_invisit%3Dtrue%7C1499225410331%3B%20s_getNewRepeat%3D1499223610336-Repeat%7C1501815610336%3B; s_sess=%20s_ctq%3D0%3B%20s_cc%3Dtrue%3B%20c%3DundefinedDirect%2520LoadDirect%2520Load%3B%20s.prop69%3Dvisitnumber_1%3B%20s_sq%3D%3B'),
                     ('upgrade-insecure-requests', '1')
                     ]

    br.open(url)
    print br.response
    s = requests.session()

    text = s.get(url, headers=header).text
    print text
    selector = Selector(text=text)
    print len((selector.css('div.mktgrp > * >table')))
    print len((selector.css('div.mktgrp > * >h3')))
    player_odds_list = []
    club_odds = []
    # for index, player in enumerate(selector.css('div.mktgrp > * >h3')):
    #     en_name = player.css('::text')[0].extract().encode('utf-8').strip()
    #     cn_name = ''
    #
    #     try:
    #         player = Player.objects.get(en_name=en_name)
    #         cn_name = player.cn_name
    #     except Player.DoesNotExist:
    #         cn_name = translate(str(player.css('::text')[0].extract().encode('utf-8').strip()))
    #         player = Player(en_name=en_name, cn_name=cn_name)
    #         print 'new player' + en_name
    #         player.save()
    #     clubs = selector.css('div.mktgrp > *>table')[index].css('td>a>span::text').extract()
    #     clubs = [
    #         str(club).replace("(Does not include returning on loan following a permanent deal elsewhere)", "").encode(
    #             'utf-8').strip() for club in clubs]
    #     clubs_cn = []
    #     for club in clubs:
    #         if club in club_name_dict:
    #             club = club_name_dict[club]
    #         club_en_name = club
    #         club_cn_name = ''
    #         try:
    #             c = Club.objects.get(en_club_name=club_en_name)
    #             club_cn_name = c.cn_club_name
    #         except Club.DoesNotExist:
    #             club_cn_name = translate(club_en_name)
    #             print 'new club' + club_en_name
    #             c = Club(en_club_name=club_en_name, cn_club_name=club_cn_name)
    #             c.save()
    #         clubs_cn.append(club_cn_name)
    #
    #     odds = selector.css('div.mktgrp > *>table')[index].css('td>a>b::text').extract()
    #     # print dict(zip(clubs, odds))
    #     # for player in selector.css('div.mktgrp >*>h3::text').extract():
    #     # 	print player.strip()
    #     player_odds = {'player': cn_name, 'odds': [dict(zip(['club', 'odd'], row)) for row in zip(clubs_cn, odds)]}
    #     player_odds_list.append(player_odds)
    #     items = [dict(zip(['club', 'odd', 'player'], row)) for row in
    #              zip(clubs_cn, odds, [cn_name] * len(clubs_cn))]
    #     club_odds += items
    # keyfunc = operator.itemgetter("club")
    # club_rumors_list = [{'club': key, 'rumors': list(grp)} for key, grp in groupby(sorted(club_odds, key=keyfunc),
    #                                                                                key=keyfunc)]
    # bo = BetOdds(odds=player_odds_list, club_rumors=club_rumors_list)
    # bo.save()


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


job()
