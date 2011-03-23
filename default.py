import urllib,urllib2,re,xbmcplugin,xbmcgui

#SC2CASTS - by You 2008.
#http://code.google.com/p/xbmc-addons/source/browse/addons/plugin.video.karaokeplay/default.py?r=1857


def CATEGORIES():
        addDir('Latest','http://sc2casts.com/all',1,'')
        addDir('Top 24h','http://sc2casts.com/top',1,'')
        addDir('Top Week','http://sc2casts.com/top?week',1,'')
        addDir('Top Month','http://sc2casts.com/top?month',1,'')
        
                       
def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="cast(.+?)"><b >(.+?)</b> vs <b >(.+?)</b>.+?\((.+?)\).+?event_name.+?>(.+?)<.+?round_name">(.+?)<.+?caster_name">(.+?)<.+?source_name">@ (.+?)<').findall(link)
        for url, p1, p2, matches, eventname, roundname, caster, source in match:
            if source == "YouTube":
                addDir(p1+" vs "+p2+" ("+matches+") ("+eventname+":"+roundname+")"+" ("+caster+")","http://sc2casts.com/cast"+url,2,'')

def VIDEOLINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()

        match = re.compile('<div id="g(.+?)"(.+?)</div></div>').findall(link)
        if len(match) > 0:
                for number, content in match:
                        match2=re.compile('<embed src="http://www.youtube.com/v/(.+?)\?').findall(content)
                        print(len(match2))
                        if len(match2) == 0:
                                addDir("Game %s" % number, 'oHg5SJYRHA0', 3,'', False)
                        if len(match2) == 1:
                                addDir("Game %s" % number, match2[0],3,'',False)
                        if len(match2) > 1:
                                for counter, videoid in enumerate(match2):
                                        addDir("Game %s, Part %s" % (number,(counter+1)), videoid,3,'',False)
        else:
                match=re.compile('<embed src="http://www.youtube.com/v/(.+?)\?').findall(link)
                if len(match) > 1:
                        for counter, videoid in enumerate(match):
                                addDir("Game 1, Part %s" % (counter+1), videoid,3,'',False)
                else:
                        addDir("Game 1", match[0],3,'',False)

def PLAYVIDEO(videoid):
        url = "plugin://plugin.video.youtube/?path=/root/search&action=play_video&videoid=%s" % videoid
        xbmc.executebuiltin('XBMC.PlayMedia(%s)' % url)
        
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param




def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage,isfolder=True):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isfolder)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)
        
elif mode==2:
        print ""+url
        VIDEOLINKS(url,name)

elif mode==3:
        print ""+url
        PLAYVIDEO(url)

#navigator = navigation.YouTubeNavigation()
#core = YouTubeCore.YouTubeCore();
#params = {}
#params["videoid"] = "lL8ix3W6t8I" 
#navigator.playVideo(params);
#(video, status) = core.construct_video_url(params);
#print video
#addLink(video["Title"], video["video_url"],"");		

xbmcplugin.endOfDirectory(int(sys.argv[1]))
