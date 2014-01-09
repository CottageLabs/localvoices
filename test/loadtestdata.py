from portality.models import Song, Singer, Version
from portality.models import SongIndex
from portality import settings
from portality.dao import LV_DAO
import esprit

# registries of the ids that we will want to index
song_ids = []
singer_ids = []
version_ids = []

# Initialise the index and push the mappings
############################################

LV_DAO.initialise_index(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, mappings=settings.MAPPINGS)

############################################
# STORAGE
############################################

# construct singer records and save them
#########################################

"""
1	Rab		Morrison	Robert? Morrison	M	Northrigg, West Lothian	Blackridge, West Lothian	1908	1967	Miner.		SoSS via Tobar an Dualchais : http://www.tobarandualchais.co.uk/en/person/3473
2	Mickey		McDaid	Michael? McDaid	M	Hillside, Inishowen, Ireland				Farmer.		Jimmy McBride, 'My Parents Reared Me Tenderly', pp. 37-38
3			Stravaig (Group)		F	Dumfries & Galloway				Folk song group whose members included Phyllis Martin, Susan Kelly, Jean McMonies, Moira Greenwood		http://www.scottishmusiccentre.com/directory/r737/
4	Peter		Fairbairn		M		Kilmarnock			Began singing in 1975, with a particular interest in songs from the south-west of Scotland.		Sheila Douglas, 'Come Gie's a Sang', p. 147.
5	Jack		McCaig		M	Borgue, Dumfries & Galloway			2000	Farmer.		Personal communication Local Voices by James Brown / http://www.footstompin.com/forum/1/21451/1
6	Sheila		Stewart		F	Blairgowrie, Perthshire		1935		Traveller singer, storyteller and author. Member of the famous Stewarts of Blair family.	[YES]	SoSS via Tobar an Dualchais: http://www.tobarandualchais.co.uk/en/person/818
7	Jeannie		Robertson	Christina Regina Higgins	F	Aberdeen		1908	1975	Famed Traveller singer.	[YES]	http://projects.scottishcultureonline.com/hall-of-fame/jeannie-robertson-mbe/
8	Hamish		Robb	James Robb	M	Wellbank, Angus	Forfar, Angus	1937		Ex-farm worker and hauler. Born in Wellbank, worked in East Lothian and the Borders before settling in Forfar.	[YES]	Local Voices, with contributor's permission
"""

# Rab Morrison
singer = Singer()
singer.lv_id = "1"
singer.set_name("Rab", None, "Morrison", "Robert Morrison")
singer.gender = "male"
singer.add_location(relation="native_area", name="Northrigg, West Lothian")
singer.add_location(relation="significant", name="Blackridge, West Lothian")
singer.born = "1908"
singer.died = "1967"
singer.biography = "Miner"
# singer.photo_url = ""
singer.source = "SoSS via Tobar an Dualchais : http://www.tobarandualchais.co.uk/en/person/3473"
singer.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
singer_ids.append(singer.id)

# Mickey McDaid
singer = Singer()
singer.lv_id = "2"
singer.set_name("Mickey", None, "McDaid", "Michael McDaid")
singer.gender = "male"
singer.add_location(relation="native_area", name="Hillside, Inishowen, Ireland")
singer.biography = "Farmer"
# singer.photo_url = ""
singer.source = "Jimmy McBride, 'My Parents Reared Me Tenderly', pp. 37-38"
singer.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
singer_ids.append(singer.id)

# Stravaig (Group)
singer = Singer()
singer.lv_id = "3"
singer.groups = "Stravaig"
singer.gender = "female"
singer.add_location(relation="native_area", name="Dumfries & Galloway")
singer.biography = "Folk song group whose members included Phyllis Martin, Susan Kelly, Jean McMonies, Moira Greenwood"
# singer.photo_url = ""
singer.source = "http://www.scottishmusiccentre.com/directory/r737/"
singer.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
singer_ids.append(singer.id)

# Peter Fairbairn
singer = Singer()
singer.lv_id = "4"
singer.set_name("Peter", None, "Fairbairn")
singer.gender = "male"
singer.add_location(relation="significant", name="Kilmarnock")
singer.biography = "Began singing in 1975, with a particular interest in songs from the south-west of Scotland."
# singer.photo_url = ""
singer.source = "Sheila Douglas, 'Come Gie's a Sang', p. 147."
singer.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
singer_ids.append(singer.id)

# Jack McCaig
singer = Singer()
singer.lv_id = "5"
singer.set_name("Jack", None, "McCaig")
singer.gender = "male"
singer.add_location(relation="native_area", name="Borgue, Dumfries & Galloway")
singer.died = "2000"
singer.biography = "Farmer"
# singer.photo_url = ""
singer.source = "Personal communication Local Voices by James Brown / http://www.footstompin.com/forum/1/21451/1"
singer.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
singer_ids.append(singer.id)

# Sheila Stewart
singer = Singer()
singer.lv_id = "6"
singer.set_name("Sheila", None, "Stewart")
singer.gender = "female"
singer.add_location(relation="native_area", name="Blairgowrie, Perthshire")
singer.born = "1935"
singer.biography = "Traveller singer, storyteller and author. Member of the famous Stewarts of Blair family."
# singer.photo_url = ""
singer.source = "SoSS via Tobar an Dualchais: http://www.tobarandualchais.co.uk/en/person/818"
singer.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
singer_ids.append(singer.id)

# Jeannie Robertson
singer = Singer()
singer.lv_id = "7"
singer.set_name("Jeannie", None, "Robertson", "Christina Regina Higgins")
singer.gender = "female"
singer.add_location(relation="native_area", name="Aberdeen")
singer.born = "1908"
singer.died = "1975"
singer.biography = "Famed Traveller singer"
# singer.photo_url = ""
singer.source = "http://projects.scottishcultureonline.com/hall-of-fame/jeannie-robertson-mbe/"
singer.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
singer_ids.append(singer.id)

# Hamish Robb
singer = Singer()
singer.lv_id = "8"
singer.set_name("Hamish", None, "Robb", "James Robb")
singer.gender = "male"
singer.add_location(relation="native_area", name="Wellbank, Angus")
singer.add_location(relation="significant", name="Forfar, Angus")
singer.born = "1937"
singer.biography = "Ex-farm worker and hauler. Born in Wellbank, worked in East Lothian and the Borders before settling in Forfar."
# singer.photo_url = ""
singer.source = "Local Voices, with contributor's permission"
singer.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
singer_ids.append(singer.id)


# construct song records and save them
######################################

"""
Falkirk Hiring Fair	Falkirk Fair	Bothy song in which man is hired to work at a farm near Falkirk, and is critical of the treatment he receives.	Falkirk	Late 19th / Early 20th Century		LV1	LV2; LV3
							
Dumfries Hiring Fair		Bothy song in which man is hired to work at a farm near Dumfries, and is critical of the treatment he receives.	Dumfries	Late 19th / Early 20th Century		LV2	LV1; LV3
							
The Boreland of Balmaghie	Parker of the Boreland	Bothy song in which man is hired to work at a farm near Castle Douglas, and is critical of the treatment he receives.	Castle Douglas	Late 19th / Early 20th Century		LV3	LV1; LV2
Andrew Lammie	Mill o Tifty's Annie	Song of tragic love between Andrew Lammie, the Laird o Fyvie's trumpeter and Mill o Tifty's Annie. Annie's parents disapprove, and have Andrew dismissed and sent away, then kill their daughter for shaming them.		Late 17th century		LV4	
							
The Bonnie Hoose o Airlie		Ballad of feuding lords. Airlie Castle is burned to the ground by Archibald Campbell, while his rival, James Ogilvie, is away.	Airlie, Angus	Mid 16th century		LV5	
The Laird o Drum		Ballad of marriage between social classes.	Drum Castle, Drumoak, Aberdeenshire	Mid 16th century		LV6	
The Cauld Water Well		Sentimental pastoral song celebrating a local wishing well.	Dundee	Late 19th century		LV7	
"""

# Falkirk Hiring Fair
song1 = Song()
song1.title = "Falkirk Hiring Fair"
song1.summary = "Bothy song in which man is hired to work at a farm near Falkirk, and is critical of the treatment he receives."
song1.add_location(relation="main", name="Falkirk")
song1.set_time_period("Late 19th Century", "Early 20th Century")
song1.lv_id = "LV1"
song1.id = song1.makeid()
song_ids.append(song1.id)
# we need the ids of the related songs, which we add get later

# Dumfries Hiring Fair
song2 = Song()
song2.title = "Dumfries Hiring Fair"
song2.summary = "Bothy song in which man is hired to work at a farm near Dumfries, and is critical of the treatment he receives."
song2.add_location(relation="main", name="Dumfries")
song2.set_time_period("Late 19th Century", "Early 20th Century")
song2.lv_id = "LV2"
song2.id = song2.makeid()
song_ids.append(song2.id)
# we need the ids of the related songs, which we add get later

# The Boreland of Balmaghie
song3 = Song()
song3.title = "The Boreland of Balmaghie"
song3.summary = "Bothy song in which man is hired to work at a farm near Castle Douglas, and is critical of the treatment he receives."
song3.add_location(relation="main", name="Castle Douglas")
song3.set_time_period("Late 19th Century", "Early 20th Century")
song3.lv_id = "LV3"
song3.id = song3.makeid()
song3.songs = [song1.id, song2.id]
song_ids.append(song3.id)

# add the relations for song1 and song2
song1.songs = [song2.id, song3.id]
song2.songs = [song1.id, song3.id]

# save all three
song1.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
song2.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
song3.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)

# Andrew Lammie
song = Song()
song.title = "Andrew Lammie"
song.summary = "Song of tragic love between Andrew Lammie, the Laird o Fyvie's trumpeter and Mill o Tifty's Annie. Annie's parents disapprove, and have Andrew dismissed and sent away, then kill their daughter for shaming them."
song.set_time_period("Late 17th Century")
song.lv_id = "LV4"
song.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
song_ids.append(song.id)


# The Bonnie Hoose o Airlie
song = Song()
song.title = "The Bonnie Hoose o Airlie"
song.summary = "Ballad of feuding lords. Airlie Castle is burned to the ground by Archibald Campbell, while his rival, James Ogilvie, is away."
song.add_location(relation="main", name="Arlie, Angus")
song.set_time_period("Mid 16th century")
song.lv_id = "LV5"
song.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
song_ids.append(song.id)

# The Laird o Drum
song = Song()
song.title = "The Laird o Drum"
song.summary = "Ballad of marriage between social classes."
song.add_location(relation="main", name="Drum Castle, Drumoak, Aberdeenshire")
song.set_time_period("Mid 16th century")
song.lv_id = "LV6"
song.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
song_ids.append(song.id)

# The Cauld Water Well
song = Song()
song.title = "The Cauld Water Well"
song.summary = "Sentimental pastoral song celebrating a local wishing well."
song.add_location(relation="main", name="Dundee")
song.set_time_period("Late 19th century")
song.lv_id = "LV7"
song.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
song_ids.append(song.id)

# construct version records and save them
##########################################

"""
LV1.1	Falkirk Fair			Scots	Rab Morrison	Hamish Henderson	1962.05	School of Scottish Studies Sound Archive, SA1962.016.A9	Falkirk			10368				Fragments only	bothy; farm; bawdy	http://www.tobarandualchais.co.uk/fullrecord/23006/1 	 	
LV1.2	Falkirk Fair			Scots	Mickey McDaid	Jimmy McBride	1985.02	Jimmy McBride, 'My Parents Reared Me Tenderly', 1985, pp. 37-38	Falkirk			10368				Only complete version known.	bothy; farm	http://www.itma.ie/inishowen/song/falkirk_fair_mickey_mcdaid	 	 
LV2.1	Dumfries Hiring Fair			Scots	Stravaig (group)	Phyllis Martin	[unknown]	Movin' on' CD Album [CDTRAX074], 1994	Dumfries								bothy; farm			
LV2.2	Dumfries Hiring Fair			Scots	Peter Fairbairn	Sheila Douglas	1995	Come Gie's a Sang', Sheila Douglas, 1995, p. 31	Dumfries			11283					bothy; farm			
LV3.1	The Boreland of Balmaghie	Parker of the Boreland		Scots	Jack McCaig	James Brown	c. 2000	Footstompin' forum: http://www.footstompin.com/forum/1/21451/1	Castle Douglas	Boreland of Balmaghie							bothy; farm	http://www.footstompin.com/forum/1/21451/1	[YES]	
LV4.1	Andrew Lammie			Scots	Sheila Stewart	Hamish Henderson	1953	School of Scottish Studies Sound Archive, SA1953.238.A7	Fyvie	Mill of Tifty		98	1018	233		Fragment only. Other instances of same singer's version: [other urls]	love; tragedy; murder	http://www.tobarandualchais.co.uk/fullrecord/26090/1	 	
LV4.2	Andrew Lammie	Mill o Tifty's Annie		Scots	Jeannie Robertson	Hamish Henderson & Jean Ritchie	1953.09	School of Scottish Studies Sound Archive, SA1953.197.5	Fyvie	Mill of Tifty		98	1018	233		21 verses.	love; tragedy; murder	http://www.tobarandualchais.co.uk/fullrecord/24187/1  /  http://canmore.rcahms.gov.uk/en/site/19194/details/mill+of+tifty+waterwheel/	 	[Yes]
LV5.1	The Bonnie Hoose o Airlie			Scots	Jeannie Robertson	Hamish Henderson & Jean Ritchie	1952	School of Scottish Studies Sound Archive, SA1952.043.A10	Airlie, Angus			794	233	199		6 verses.	murder; castle; arson	http://www.tobarandualchais.co.uk/fullrecord/49656/1	 	
LV6.1	The Laird o Drum			Scots	Jeannie Robertson	Hamish Henderson & Jean Ritchie	1962.05	School of Scottish Studies Sound Archive, SA1962.013.A11	Drum Castle, Drumoak, Aberdeenshire			247	835	236		Fragment only.	marriage; social class	http://www.tobarandualchais.co.uk/fullrecord/23305/1	 	[Yes]
LV7.1	The Cauld Water Well			Scots / English	Hamish Robb	Local Voices	2013.08.24	Local Voices Sound Archive [local ref]	Dundee							No other source known. Also recorded but with fewer verses on Local Voices Sound Archive refs [refs.]	wishing well; river			
"""

# Falkirk Fair (LV1.1)

version = Version()
version.lv_id = "LV1.1"
version.title = "Falkirk Fair"
version.language = "Scots"
version.singer = singer_ids[0] # Rab Morrison
version.collector = "Hamish Henderson"
version.collected_date = "1962-05"
version.source = "School of Scottish Studies Sound Archive, SA1962.016.A9"
version.add_location(name="Falkirk")
version.add_reference("ROUD", "10368")
version.comments = "Fragments only"
version.tags = ["bothy", "farm", "bawdy"]
version.media_url = "http://www.tobarandualchais.co.uk/fullrecord/23006/1"
# version.lyrics = ""
# version.photo_url = ""
version.song = song_ids[0]
version.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
version_ids.append(version.id)

# Falkirk Fair (LV1.2)

version = Version()
version.lv_id = "LV1.2"
version.title = "Falkirk Fair"
version.language = "Scots"
version.singer = singer_ids[1] # Mickey McDaid
version.collector = "Jimmy McBride"
version.collected_date = "1985-02"
version.source = "Jimmy McBride, 'My Parents Reared Me Tenderly', 1985, pp. 37-38"
version.add_location(name="Falkirk")
version.add_reference("ROUD", "10368")
version.comments = "Only complete version known"
version.tags = ["bothy", "farm"]
version.media_url = "http://www.itma.ie/inishowen/song/falkirk_fair_mickey_mcdaid"
# version.lyrics = ""
# version.photo_url = ""
version.song = song_ids[0]
version.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
version_ids.append(version.id)

# Dumfries Hiring Fair (LV2.1)

version = Version()
version.lv_id = "LV2.1"
version.title = "Dumfries Hiring Fair"
version.language = "Scots"
version.singer = singer_ids[2] # Stravaig
version.collector = "Phyllis Martin"
# version.collected_date = ""
version.source = "Movin' on' CD Album [CDTRAX074], 1994"
version.add_location(name="Dumfries")
# version.add_reference("", "")
# version.comments = ""
version.tags = ["bothy", "farm"]
# version.media_url = ""
# version.lyrics = ""
# version.photo_url = ""
version.song = song_ids[1]
version.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
version_ids.append(version.id)


# Dumfries Hiring Fair (LV2.2)

version = Version()
version.lv_id = "LV2.2"
version.title = "Dumfries Hiring Fair"
version.language = "Scots"
version.singer = singer_ids[3] # Peter Fairbairn
version.collector = "Sheila Douglas"
version.collected_date = "1995"
version.source = "Come Gie's a Sang', Sheila Douglas, 1995, p. 31"
version.add_location(name="Dumfries")
version.add_reference("ROUD", "11283")
# version.comments = ""
version.tags = ["bothy", "farm"]
# version.media_url = ""
# version.lyrics = ""
# version.photo_url = ""
version.song = song_ids[1]
version.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
version_ids.append(version.id)

# The Boreland of Balmaghie (LV3.1)

version = Version()
version.lv_id = "LV3.1"
version.title = "The Boreland of Balmaghie"
version.alternative_title = "Parker of the Boreland"
version.language = "Scots"
version.singer = singer_ids[4] # Jack McCaig
version.collector = "James Brown"
version.collected_date = "c. 2000"
version.source = "Footstompin' forum: http://www.footstompin.com/forum/1/21451/1"
version.add_location(name="Castle Douglas")
version.add_location(name="Boreland of Balmaghie")
# version.add_reference("", "")
# version.comments = ""
version.tags = ["bothy", "farm"]
version.media_url = "http://www.footstompin.com/forum/1/21451/1"
# version.lyrics = ""
# version.photo_url = ""
version.song = song_ids[2]
version.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
version_ids.append(version.id)

# Andrew Lammie (LV4.1)

version = Version()
version.lv_id = "LV4.1"
version.title = "Andrew Lammie"
# version.alternative_title = ""
version.language = "Scots"
version.singer = singer_ids[5] # Sheila Stewart
version.collector = "Hamish Henderson"
version.collected_date = "1953"
version.source = "School of Scottish Studies Sound Archive, SA1953.238.A7"
version.add_location(name="Fyvie")
version.add_location(name="Mill of Tifty")
version.add_reference("ROUD", "98")
version.add_reference("Greig-Duncan", "1018")
version.add_reference("Child", "233")
version.comments = "Fragment only. Other instances of same singer's version: [other urls]"
version.tags = ["love", "tragedy", "murder"]
version.media_url = "http://www.tobarandualchais.co.uk/fullrecord/26090/1"
# version.lyrics = ""
# version.photo_url = ""
version.song = song_ids[3]
version.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
version_ids.append(version.id)

# Andrew Lammie (LV4.2)

version = Version()
version.lv_id = "LV4.2"
version.title = "Andrew Lammie"
version.alternative_title = "Mill o Tifty's Annie"
version.language = "Scots"
version.singer = singer_ids[6] # Jeannie Robertson
version.collector = "Hamish Henderson & Jean Ritchie"
version.collected_date = "1953-09"
version.source = "School of Scottish Studies Sound Archive, SA1953.197.5"
version.add_location(name="Fyvie")
version.add_location(name="Mill of Tifty")
version.add_reference("ROUD", "98")
version.add_reference("Greig-Duncan", "1018")
version.add_reference("Child", "233")
version.add_reference("Laws", "21")
version.comments = "verses"
version.tags = ["love", "tragedy", "murder"]
version.media_url = ["http://www.tobarandualchais.co.uk/fullrecord/24187/1", "http://canmore.rcahms.gov.uk/en/site/19194/details/mill+of+tifty+waterwheel/"]
# version.lyrics = ""
# version.photo_url = ""
version.song = song_ids[3]
version.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
version_ids.append(version.id)


# The Bonnie Hoose o Airlie (LV5.1)

version = Version()
version.lv_id = "LV5.1"
version.title = "The Bonnie Hoose o Airlie"
# version.alternative_title = ""
version.language = "Scots"
version.singer = singer_ids[6] # Jeannie Robertson
version.collector = "Hamish Henderson & Jean Ritchie"
version.collected_date = "1952"
version.source = "School of Scottish Studies Sound Archive, SA1952.043.A10"
version.add_location(name="Airlie, Angus")
version.add_reference("ROUD", "794")
version.add_reference("Greig-Duncan", "233")
version.add_reference("Child", "299")
version.add_reference("Laws", "6")
version.comments = "6 verses"
version.tags = ["castle", "arson", "murder"]
version.media_url = "http://www.tobarandualchais.co.uk/fullrecord/49656/1"
# version.lyrics = ""
# version.photo_url = ""
version.song = song_ids[4]
version.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
version_ids.append(version.id)

# The Laird o Drum (LV6.1)

version = Version()
version.lv_id = "LV6.1"
version.title = "The Laird o Drum"
# version.alternative_title = ""
version.language = "Scots"
version.singer = singer_ids[6] # Jeannie Robertson
version.collector = "Hamish Henderson & Jean Ritchie"
version.collected_date = "1962-05"
version.source = "School of Scottish Studies Sound Archive, SA1962.013.A11"
version.add_location(name="Drum Castle, Drumoak, Aberdeenshire")
version.add_reference("ROUD", "247")
version.add_reference("Greig-Duncan", "835")
version.add_reference("Child", "236")
version.comments = "Fragment only"
version.tags = ["marriage", "social class"]
version.media_url = "http://www.tobarandualchais.co.uk/fullrecord/23305/1"
# version.lyrics = ""
# version.photo_url = ""
version.song = song_ids[5]
version.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
version_ids.append(version.id)


# The Cauld Water Well (LV7.1)

version = Version()
version.lv_id = "LV7.1"
version.title = "The Cauld Water Well"
# version.alternative_title = ""
version.language = ["Scots", "English"]
version.singer = singer_ids[7] # Hamish Robb
version.collector = "Local Voices"
version.collected_date = "2013-08-24"
version.source = "Local Voices Sound Archive [local ref]"
version.add_location(name="Dundee")
# version.add_reference("", "")
version.comments = "No other source known. Also recorded but with fewer verses on Local Voices Sound Archive refs [refs.]"
version.tags = ["wishing well", "river"]
# version.media_url = ""
# version.lyrics = ""
# version.photo_url = ""
version.song = song_ids[6]
version.save(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB, refresh=True)
version_ids.append(version.id)



###################################################
# INDEXING
###################################################

# connection object to use for the save operations
conn = esprit.raw.Connection(host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB)

# index all the songs
#####################

for sid in song_ids:
    song = Song().get(sid, links=True, host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB)
    si = SongIndex.from_song(song)
    si.save(conn=conn)

# index all the singers
#######################

for sid in singer_ids:
    singer = Singer().get(sid, links=True, host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB)
    si = SingerIndex.from_singer(singer)
    si.save(conn=conn)

# index all the versions
########################

for vid in version_ids:
    version = Version().get(vid, links=True, host=settings.ELASTIC_SEARCH_HOST, index=settings.ELASTIC_SEARCH_DB)
    vi = VersionIndex.from_version(version)
    vi.save(conn=conn)



