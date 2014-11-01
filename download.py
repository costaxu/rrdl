#!/usr/bin/env python
#coding: utf-8
import urllib2, os, re, json, chardet, traceback, sys, time
reload(sys)
sys.setdefaultencoding('utf-8')

cookie = os.environ['cookie']
headers = {}
headers["Cookie"] = cookie
print cookie
g_download_fail_count = 0
g_download_success_count = 0
g_download_fail_list = []
g_parse_albumn_success_count = 0
g_parse_albumn_fail_count = 0
g_parse_albumn_fail_list = []

def SavePhoto(aid, pid, purl, ptitle):
  global g_download_success_count
  global g_download_fail_count
  global g_download_fail_list
  dirname = os.path.join("data" , aid)
  if not os.path.exists(dirname):
    os.makedirs(dirname)
  download_success = False
  for i in range(0,3):
    try:
      print purl
      photo_content = urllib2.urlopen(purl).read()
      download_success = True
      break
    except Exception: 
      print "download fail, sleep 3 seconds"
      time.sleep(3) 
  if not download_success:
    g_download_fail_count += 1
    g_download_fail_list.append(purl)
    return
  filename = os.path.join(dirname.decode("utf-8"), pid+ ".jpg") 
  f = open(filename, 'w')
  f.write(photo_content)
  f.close()
  filename = os.path.join(dirname, pid + '.txt')
  f = open(filename, 'w')
  print ptitle
  print chardet.detect(ptitle)
  f.write(ptitle)
  f.close()
  g_download_success_count +=1

def DownloadAlbumn(url):
  url = url.strip("\n")
  albumn_id = url.split("-")[1]
  dirname = os.path.join("data" , albumn_id)
  if not os.path.exists(dirname):
    os.makedirs(dirname)
  print url
  request = urllib2.Request(url , headers = headers)  
  response = urllib2.urlopen(request, timeout = 5).read()
  m = re.search('<title>(.*)</title>', response) 
  if m:
    albumn_title = m.group(1)
    splits = albumn_title.split(' - ')
    if len(splits) >= 3:
      albumn_title = splits[2].strip()
      filename = os.path.join("data", albumn_id, "albumn.txt")
      f = open(filename, 'w') 
      f.write(albumn_title)
      f.close()
  for i in range(0,10):
    ajax_url = url + "/bypage/ajax?curPage=%d&pagenum=20" % i
    print ajax_url
    request = urllib2.Request(ajax_url , headers = headers)  
    response = urllib2.urlopen(request, timeout = 5).read()
    json_object = json.loads(response)
    for photo in json_object['photoList']:
      photo_url = photo["xLarge"]
      if not photo_url:
        photo_url = photo["largeUrl"]
      photo_title = photo["title"] 
      photo_id = photo["photoId"]
      SavePhoto(albumn_id, photo_id, photo_url, photo_title)
      print "downloaded " + photo_url

if __name__ == "__main__":
  time1 = int(time.time())
  i = 0
  for url in open("albumn.final.txt"):
    try:
      i += 1
      print "albumn %d" % i
      DownloadAlbumn(url)
      g_parse_albumn_success_count += 1
    except Exception, e:
      print traceback.format_exc(e)
      g_parse_albumn_fail_count += 1
      g_parse_albumn_fail_list.append(url) 
  print "-"*30
  print "parse albumn success count: %d" % (g_parse_albumn_success_count)
  print "parse albumn fail count: %d" % (g_parse_albumn_fail_count)
  for url in g_parse_albumn_fail_list:
    print url
  print "-"*30
  print "Download success count: %d" % (g_download_success_count)
  print "Download fail count: %d" % (g_download_fail_count)
  for url in g_download_fail_list:
    print url
  print "-"*30
  time2 = int(time.time())
  print "time: %d seconds" % (time2 - time1) 
  #SavePhoto("test", "test", "http://fmn.rrfmn.com/fmn059/20130513/1505/large_xNdo_1b9900004a9a118c.jpg")
  #DownloadAlbumn("http://photo.renren.com/photo/200308079/album-364858531")
