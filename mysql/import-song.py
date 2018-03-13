#!/usr/bin/env python
# -*- coding:utf-8 -*-
#actor_data = 'REPLACE INTO karaok.actors (actor_no,actor_name,actor_des,actor_type,actor_py,actor_jp,actor_click,actor_clickw,actor_clickm) VALUES({}|{}|{}|{}|{}|{}|{}|{}|{});'
actor_data = '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n'
#media_data = 'REPLACE INTO karaok.medias(media_no,media_name,media_namelen,media_langid,media_lang,media_tag,media_tag1,media_tag2,media_actname1,media_actname2,media_actname3,media_actname4,media_carria,media_yuan,media_ban,media_svrgroup,media_file,media_style,media_audio,media_volume,media_jp,media_py,media_strok,media_stroks,media_lyric,media_isnew,media_clickm,media_clickw,media_click,media_type,media_stars,media_actno1,media_actno2,media_actno3,media_actno4,media_dafen,media_climax,media_climaxinfo,media_yinyi,media_light) VALUES({}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{});'
media_data = '{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}'
def load_carriers():
    carriers = {'DVD': '2', 'MPEG1': '3', 'MPEG2':'4', 'SVCD':'5', 'MP3': '6', 'WAV': '7', 'LS':'8', 'LSS':'9', 'WAV':'10'}
    return carriers

def get_actortype_id(actype):
    if actype == '大陆男歌星':
        return 1
    elif actype == '大陆女歌星':
        return 2
    elif actype == '港台男歌星':
        return 3
    elif actype == '港台女歌星':
        return 4
    elif actype == '外国歌星':
        return 5
    elif actype == '中国组合':
        return 6
    elif actype == '外国组合':
        return 7
    elif actype == '影星':
        return 8



def get_langid(lang):
    if lang == '国语':
        return 2
    elif lang == '粤语':
        return 3
    elif lang == '闽南语':
        return 4
    elif lang == '英语':
        return 5
    elif lang == '日语':
        return 6
    elif lang == '韩语':
        return 7
    elif lang == '其它':
        return 8

def load_videotype():
    v_types = ['流水影', 'MV', '演唱会']
    return v_types

def parse_actors(actinfo, actnos):
    acts = {}
    #actnos = actnos.split(',')
    if not actinfo:
        return []

    arr = actinfo.split(',')
    if len(arr) % 4 != 0 or len(arr) < 4:
        return []
    i = 0
    for i in range(0, len(actnos)):
        act = {}
        j = i*4
        act['name'] = arr[j]
        act['des'] = arr[j]
        act['type'] = arr[j+1]
        act['typeid'] = get_actortype_id(act['type'])
        act['py'] = arr[j+2]
        act['jp'] = arr[j+3]
        acts[actnos[i]] = act
    return acts

def parseinfo(fname):
    act_fp = open('actors.data', 'w+')
    media_fp = open('medias.data', 'w+')
    videotypes = load_videotype()
    act_list = []
    try:
        fp = open(fname)
    except Exception as ex:
        print('Failed to open file')
        return
    for line in fp:
        line = line.strip()
        arr = line.split('|')
        if len(arr) < 20:
            continue
        if arr[0] == '广告':
            media_type = '2'
        elif arr[0] == '电影':
            media_type = '3'
        else:
            media_type = '1'

        media_name = arr[1]
        media_lang = arr[2]
        media_langid = get_langid(media_lang)
        media_tags = arr[3]
        media_tag1 = ''
        media_tag2 = ''
        tags = media_tags.split(',')
        index = len(tags)
        if index > 0:
            media_tag1 = tags[0]
        if index > 1:
            media_tag2 = tags[1]

        #载体DVD等等
        media_carria = arr[5]
        #原唱左声道
        media_yuan = arr[6]
        #伴唱右声道
        media_ban = arr[7]
        #maybe the filepath
        media_file = arr[8]
        fno = media_file.split('.')
        media_no = fno[0]
        media_videotype = arr[9]
        media_volume = arr[10]
        media_audio = arr[11]
        media_jp = arr[12]
        media_namelen = str(len(media_jp))
        media_langtype = arr[13]
        media_stroke = arr[14]
        media_strokes = arr[15]
        #media_heng = arr[15]
        media_py = arr[19]

        media_actno1 = '0'
        media_actno2 = '0'
        media_actno3 = '0'
        media_actno4 = '0'

        media_actname1 = ''
        media_actname2 = ''
        media_actname3 = ''
        media_actname4 = ''

        media_actnos = arr[21]
        acts = media_actnos.split(';')
        index = len(acts)
        media_actors = arr[4]
        new_acts = parse_actors(media_actors, acts)
        i = 0
        for ano in new_acts:
            if i == 0:
                media_actno1 = ano
                media_actname1 = new_acts[ano]['name']
            elif i == 1:
                media_actno2 = ano
                media_actname2 = new_acts[ano]['name']
            elif i == 2:
                media_actno3 = ano
                media_actname3 = new_acts[ano]['name']
            elif i == 3:
                media_actno4 = ano
                media_actname4 = new_acts[ano]['name']
            i += 1
            
            if ano not in act_list:
                act_list.append(ano)
                act_fp.write(actor_data.format(ano, new_acts[ano]['name'], new_acts[ano]['des'], new_acts[ano]['typeid'], new_acts[ano]['type'],new_acts[ano]['jp'], new_acts[ano]['py'], '0', '0', '0'))

        media_lyric = ''
        media_isnew = '0'
        media_click = '0'
        media_clickm = '0'
        media_clickw = '0'
        media_dafen = '0'
        media_climax = '0'
        media_climaxinfo = ''
        media_yinyi = '0'
        media_light = '0'
        media_svrgroup = '1'
        media_stars = '0'

        media_fp.write(media_data.format \
                (media_no, media_name, media_namelen, media_langtype, media_langid, media_lang,\
                media_tag1, media_tag2, media_actname1, media_actname2, media_actname3, media_actname4, media_carria, \
                media_yuan, media_ban, media_svrgroup, media_file,\
                media_videotype, media_audio, media_volume, \
                media_jp, media_py,\
                media_stroke, media_strokes, media_lyric, media_isnew, \
                media_clickm, media_clickw, media_click, \
                media_type, media_stars, media_actno1, media_actno2, media_actno3, media_actno4, \
                media_dafen, media_climax, media_climaxinfo, media_yinyi, media_light))
        media_fp.write("\n")
    act_fp.close()

def load_clickcount(fname):
    '''
    加载点击量信息
    '''
    order_info = {}
    for line in open(fname):
        txt = line.split('|')
        if len(txt) == 2:
            textNo = txt[0]
            textNo = textNo[3:]
            order = txt[1]
            order_info[textNo.strip()] = order
    return order_info

def load_clicmax(fname):
    pass

def scan_mediafiles(root='/video'):
    pass

if __name__ == '__main__':
    parseinfo('24W-medias.txt')

