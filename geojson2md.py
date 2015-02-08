import codecs
import json
import urllib
import collections

def makeObject(props):
    md_obj = '''
##%s
**%s**, %s

''' % (props['title'], props['artist'], props['address'])

    return md_obj

def makeYear(md, year, features, previous_coords):
    thumb_width = 400
    md += "#%s\n```\n" % year
    #something to set center
    #something to set zoom
    newCoords = []
    objectlist = []
    imagelist = []
    for f in features:
        newCoords.append(f['coordinates'])
        md += "L.marker([%f, %f]).setIcon(newIcon).actions.addRemove(S.map)\n" % (f['coordinates'][1], f['coordinates'][0])
        imagelist.append(f['properties']['image'])
        objectlist.append(makeObject(f['properties']))
    if previous_coords and len(previous_coords) > 0:
        for c in previous_coords:
            md += "L.marker([%f, %f]).setIcon(oldIcon).actions.addTo(S.map)\n" % (c[1], c[0])
    md += "```\n"
    #todo select a random image
    thumburl = "https://commons.wikimedia.org/w/thumb.php?%s&width=%d" % (urllib.urlencode({'f': imagelist[0].replace(' ','_').encode('utf-8')}) , thumb_width)
    linkurl = "https://commons.wikimedia.org/wiki/File:%s" % imagelist[0].replace(' ','_')
    md += "[![](%s)](%s)\n" % (thumburl, linkurl)
    for o in objectlist:
        md += o

    return newCoords, md

f = codecs.open('api.geo.json', 'r', 'utf8')
j = json.load(f)
f.close()

byYear = {}
for feature in j['features']:
    year = feature['properties']['year']
    lump = {
        'coordinates' : feature['geometry']['coordinates'],
        'properties' : feature['properties']
        }
    if year in byYear.keys():
        byYear[year].append(lump.copy())
    else:
        byYear[year] = [lump.copy(), ]

md = '''```
-title: "Public art in Stockholm"
-author: "Lokal_Profil"
-baseurl: "https://dnv9my2eseobd.cloudfront.net/v3/cartodb.map-4xtxp73f/{z}/{x}/{y}.png"
```
'''

byYear = collections.OrderedDict(sorted(byYear.items()))
prev_year = []
for k, v in byYear.iteritems():
    prev_year, md = makeYear(md, k, v, prev_year)

f = codecs.open('pubArtOdyssey.md', 'w', 'utf8')
f.write(md)
f.close()
