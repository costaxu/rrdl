#!/usr/bin/env python
#coding: utf-8
import urllib2, os, re, json, chardet
cookie = os.environ['cookie']
headers = {}
headers["Cookie"] = cookie
print cookie

def SavePhoto(atitle, ptitle, purl):
  dirname = os.path.join("data" , atitle)
  if not os.path.exists(dirname):
    os.makedirs(dirname)
  photo_content = urllib2.urlopen(purl).read()
  filename = os.path.join(dirname.decode("utf-8"), ptitle + ".jpg") 
  f = open(filename, 'w')
  f.write(photo_content)
  f.close()

def DownloadAlbumn(url):
  url = url.strip("\n")
  print url
  request = urllib2.Request(url , headers = headers)  
  response = urllib2.urlopen(request, timeout = 5).read()
  #print response
  m = re.search('<title>(.*)</title>', response) 
  if m:
    albumn_title = m.group(1)
    splits = albumn_title.split(' - ')
    if len(splits) >= 3:
      albumn_title = splits[2].strip()
      print albumn_title
      print chardet.detect(albumn_title)
  for i in range(0,10):
    ajax_url = url + "/bypage/ajax?curPage=%d&pagenum=20" % i
    print ajax_url
    request = urllib2.Request(ajax_url , headers = headers)  
    response = urllib2.urlopen(request, timeout = 5).read()
    json_object = json.loads(response)
    for photo in json_object['photoList']:
      photo_url = photo["largeUrl"]
      #photo_title = photo["title"] 
      photo_id = photo["photoId"]
      #if not photo_title:
      #  photo_title = photo_id
      SavePhoto(albumn_title, photo_id, photo_url)
      print "downloaded " + photo_url
if __name__ == "__main__":
  for url in open("albumn.final.txt"):
    DownloadAlbumn(url)
  #SavePhoto("test", "test", "http://fmn.rrfmn.com/fmn059/20130513/1505/large_xNdo_1b9900004a9a118c.jpg")
  #DownloadAlbumn("http://photo.renren.com/photo/200308079/album-364858531")
