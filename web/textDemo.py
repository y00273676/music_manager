#!/usr/bin/python
# -*- coding: UTF-8 -*-
if __name__=='__main__':
    media = {}
    media['sname1'] = ''
    media['sname2'] = ''
    media['sname3'] = ''
    media['sname4'] = ''
    line='歌曲|因为爱情|国语|影视金曲,男女对唱|陈奕迅,港台男歌星,CYX,chen_yi_xun,王菲,港台女歌星,WF,wang_fei|DVD|1|2|7409832.mpg|0|6|MPEG|YWAQ|0|6|2434|0|653171|0|yin_wei_ai_qing|0|102141;110722'
    txtArr = line.split('|')
    if txtArr[4].find(','):
        starInfo = txtArr[4].split(',')
        infoCount = len(starInfo)/4
        if infoCount == 1:
            media['sname1'] = starInfo[0].replace('\'',' ')

            media['actor_name'] = starInfo[0].replace('\'',' ')
            media['actor_typename'] = starInfo[1]
            media['actor_photo'] = ''
            media['actor_jianpin'] = starInfo[2]
            media['actor_pinyin'] = starInfo[3]
            media['actor_no'] = txtArr[21]
            
            #print media
        else:
            actorNoArr = txtArr[21].split(';')
            for k in range(infoCount):
                media['sname'+str(k+1)] = starInfo[k*4].replace('\'',' ')
                
                media['actor_name'] = starInfo[k*4].replace('\'',' ')
                media['actor_typename'] = starInfo[k*4+1]
                media['actor_photo'] = ''
                media['actor_jianpin'] = starInfo[k*4+2]
                media['actor_pinyin'] = starInfo[k*4+3]
                media['actor_no'] = actorNoArr[k]
                
                print media