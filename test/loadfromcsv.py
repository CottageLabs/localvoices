import csv, requests, json

from portality.models import Singer, Song, Version
from portality import settings

singers = "data/Singers.csv"
songs_versions = "data/SongsVersions.csv"
api = "http://localhost:5002"

SINGER_LV_ID_MAP = {}
SONG_LV_ID_MAP = {}
SONG_SONG_MAP = []

def _normalise(cell):
    return cell if cell is not None and cell != "" else None

reader = csv.reader(open(singers))
first = True
for row in reader:
    if first:
        first = False
        continue
    
    singer = Singer()
    singer.lv_id = row[0]
    
    fn = _normalise(row[1])
    ln = _normalise(row[2])
    aka = _normalise(row[3])
    singer.set_name(first=fn, last=ln, aka=aka)
    
    if row[4] is not None and row[4] != "":
        singer.gender = row[4].lower()
    
    place = _normalise(row[5])
    lat = _normalise(row[6])
    lon = _normalise(row[7])
    if place is not None or lat is not None or lon is not None:
        singer.add_location(relation="native_area", lat=lat, lon=lon, name=place)
    
    place = _normalise(row[8])
    lat = _normalise(row[9])
    lon = _normalise(row[10])
    if place is not None or lat is not None or lon is not None:
        singer.add_location(relation="significant", lat=lat, lon=lon, name=place)
    
    birth = _normalise(row[11])
    if birth is not None:
        singer.born = birth
    
    death = _normalise(row[12])
    if death is not None:
        singer.died = death
    
    bio = _normalise(row[13])
    if bio is not None:
        singer.biography = bio
    
    # skipping column 14 (photo)
    
    source = _normalise(row[15])
    if source is not None:
        singer.source = source
    
    # now save the object via the web API (to test it)
    resp = requests.post(api + "/singers", data=json.dumps({"singer" : singer.data.get("singer")}))
    print "saved singer", resp.json().get("id")
    
    # record the id and map it to the lvid for later use
    id = resp.json().get("id")
    SINGER_LV_ID_MAP[row[0]] = id

reader = csv.reader(open(songs_versions))
count = 0
for row in reader:
    if count < 2: # skip the first two lines
        count += 1
        continue
    
    # first have a go at the song that appears on this row
    slv_id = _normalise(row[5])
    if slv_id is not None and slv_id not in SONG_LV_ID_MAP.keys():
        song = Song()
        stitle = _normalise(row[0])
        if stitle is not None:
            song.title = stitle
        
        # skip row[1] - alternative title is calculated from versions later
        
        ssummary = _normalise(row[2])
        if ssummary is not None:
            song.summary = ssummary
        
        slocation = _normalise(row[3])
        if slocation is not None:
            song.add_location(relation="main", name=slocation)
        
        scomposer = _normalise(row[4])
        if scomposer is not None:
            song.composer = scomposer
        
        # row[5]
        song.lv_id = slv_id
        
        # record the song-to-song relationships required
        rel = _normalise(row[6])
        if rel is not None:
            SONG_SONG_MAP.append((slv_id, rel))
        
        # save the object via the web API (to test it)
        resp = requests.post(api + "/songs", data=json.dumps({"song" : song.data.get("song")}))
        print "saved song", resp.json().get("id")
        
        # record the id and map it to the lvid for later use
        id = resp.json().get("id")
        SONG_LV_ID_MAP[slv_id] = id
    
    # now lift the version out of this row
    version = Version()
    
    vlv_id = _normalise(row[8])
    version.lv_id = vlv_id
    
    sid = SONG_LV_ID_MAP.get(vlv_id.split(".")[0])
    version.song = sid
    
    vtitle = _normalise(row[9])
    if vtitle is not None:
        version.title = vtitle
    
    valt = _normalise(row[10])
    if valt is not None:
        version.alternative_title = valt
    
    vsummary = _normalise(row[11])
    if vsummary is not None:
        version.summary = vsummary
    
    eng = _normalise(row[12])
    if eng == "TRUE":
        version.add_language("English")
    
    gae = _normalise(row[13])
    if gae == "TRUE":
        version.add_language("Gaelic")
    
    scots = _normalise(row[14])
    if scots == "TRUE":
        version.add_language("Scots")
    
    oth = _normalise(row[15])
    if oth == "TRUE":
        version.add_language("Other")
    
    singlv = _normalise(row[16])
    if singlv is not None:
        singid = SINGER_LV_ID_MAP.get(singlv)
        version.singer = singid
    
    # rows 17 to 24 are singer data which has already been imported
    collector = _normalise(row[25])
    if collector is not None:
        version.collector = collector
    
    cdate = _normalise(row[26])
    if cdate is not None:
        cdate = cdate.replace(".", "-")
        version.collected_date = cdate
    
    vsource = _normalise(row[27])
    if vsource is not None:
        version.source = vsource
    
    loc1p = _normalise(row[28])
    loc1lat = _normalise(row[29])
    loc1lon = _normalise(row[30])
    if loc1p is not None or loc1lat is not None or loc1lon is not None:
        version.add_location(relation="main", lat=loc1lat, lon=loc1lon, name=loc1p)
    
    loc2p = _normalise(row[31])
    loc2lat = _normalise(row[32])
    loc2lon = _normalise(row[33])
    if loc2p is not None or loc2lat is not None or loc2lon is not None:
        version.add_location(lat=loc2lat, lon=loc2lon, name=loc2p)
    
    loc3p = _normalise(row[34])
    loc3lat = _normalise(row[35])
    loc3lon = _normalise(row[36])
    if loc3p is not None or loc3lat is not None or loc3lon is not None:
        version.add_location(lat=loc3lat, lon=loc3lon, name=loc3p)
    
    roud = _normalise(row[37])
    if roud is not None:
        version.add_reference("roud", roud)
    
    gd = _normalise(row[38])
    if gd is not None:
        version.add_reference("greig-duncan", gd)
    
    child = _normalise(row[39])
    if child is not None:
        version.add_reference("child", child)
    
    laws = _normalise(row[40])
    if laws is not None:
        version.add_reference("laws", laws)
    
    note = _normalise(row[41])
    if note is not None:
        version.comments = note
    
    url = _normalise(row[42])
    if url is not None:
        version.media_url = url
    
    # skip 43 - tags, 44 - lyrics and 45 - photo as no example content available
    
    # save the object via the web API (to test it)
    vobj = {
        "version" : version.data.get("version"),
        "song" : version.data.get("song"),
        "singer" : version.data.get("singer")
    }
    resp = requests.post(api + "/versions", json.dumps(vobj))
    print "saved version", resp.json().get("id")

# get the pure pair-wise relationships between songs with no duplicates
lv_rels = list(set([tuple(y) for y in [sorted(list(x)) for x in SONG_SONG_MAP]]))
rels = [(SONG_LV_ID_MAP.get(s), SONG_LV_ID_MAP.get(t)) for s, t in lv_rels]

for source, target in rels:
    req = {"id" : source, "songs" : [target]}
    resp = requests.put(api + "/song/" + source, data=json.dumps(req))
    print "created song-to-song relationship", source, "-", target


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
