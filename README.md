# Local Voices

## Search Requirements

From an API point of view, the following search operations are required:

**1/ Search for singers:**

* geographical constraint
* free-text string constraint

What does the free-text string cover: just the singer metadata or also the singer's songs?

Returns:
* A list of singers with some basic info and their lat/long

**2/ Search for songs:**

* geographical constraint
* free-text string constraint

The free-text string constraint will cover both songs and song variations

Returns:
* A list of songs with some basic info and their lat/long

**3/ All information associated with a singer**

* The singer metadata
* The list of song versions by that singer

**4/ All information associated with a song**

* The song metadata
* The list of versions of that song
* The list of singers who sung that song
* The list of related songs

**5/ Search free-text across all content**

Returns:
* A list of singers
* A list of songs

**6/ List all singers alphabetically**

Returns:
* A list of singers

## Data Model

### Singer

    {
        "id" : "<opaque internal identifier>",
        "lv_id" : "<local voices identifier>",
        "name" : {
            "first" : "<first name>",
            "middle" : "<middle name or initial>",
            "last" : "<surname>",
            "aka" : [<nicknames and translations>]
        },
        "groups" : [<list of bands/choirs>],
        "gender" : "<male|female>",
        "location" : [
            {
                "relation" : "<nature of singers relationship to place>",
                "lat" : "<latitude>",
                "long" : "<longitude>",
                "name" : "<textual name of place>"
            }
        ]
        "born" : "<(partial) datestamp>",
        "died" : "<(partial) datestamp>",
        "biography" : "<biographical summary>",
        "songs" : [<opaque identifiers of song versions>]
        "created_date" : "<created date>",
        "last_updated" : "<last updated date>"
    }

* id - the opaque system identifier for the singer; not for use by the outside world
* lv_id - The Local Voices identifier for the singer
* name - a compound attribute describing the singer's name, and name variants
* groups - bands/choirs that the singer has been associated with
* gender - gender of the singer
* location - a list of locations relevant to the singer.  Each location is a compound attribute with the lat/long and the name of the place, as well as an optional relationship the place has to the singer
* born - date the singer was born.  May be a date fragment (e.g. just the year)
* died - date the singer died (if relevant).  May be a date fragment (e.g. just the year)
* biography - free text biographical information
* songs - the list of song versions performed by this singer
* created_date - a timestamp, system assigned, for the moment the record was created
* last_updated - a timestamp, system assigned, for the last time the record was updated


### Song

    {
        "id" : "<opaque internal identifier>",
        "lv_id" : "<local voices identifier>",
        "title" : "<canonical song title>",
        "alternative_titles" : [<list of alternative song titles>],
        "summary" : "<free text summary>",
        "location": [
            {
                "relation" : "<nature of song's relationship to place>",
                "lat" : "<latitude>",
                "long" : "<longitude>",
                "name" : "<textual name of place>"
            }
        ],
        "time_period" : {
            "from" : "<partial date>",
            "to" : "<partial date>"
        },
        "composer" : "<free text name of composer>",
        "relations" : [<opaque identifier of related song>],
        "references" : [<references of all versions>],
        "versions" : [<opaque identifier of versions>],
        "created_date" : "<created date>",
        "last_updated" : "<last updated date>"
    }

* id - the opaque system identifier for the song; not for use by the outside world
* lv_id - The Local Voices identifier for the song
* title - this is the most commonly agreed-upon title for the song
* alternative_titles - this is all of the titles of the song variants
* location - a list of locations relevant to the song.  Each location is a compound attribute with the lat/long and the name of the place, as well as an optional relationship the place has to the song
* time_period - a granular date (e.g. just the year), and optionally a range using "from" and "to" (if no range, just uses "from")
* composer - name of the composer of this song
* relations - other songs which have relationships to this song (in an unspecified manner)
* classifications - list of classifications aggregated from the song variants
* versions - the list of versions of this song
* created_date - a timestamp, system assigned, for the moment the record was created
* last_updated - a timestamp, system assigned, for the last time the record was updated


### Song Version

    {
        "id" : "<opaque internal identifier>",
        "lv_id" : "<local voices identifier>",
        "title" : "<title of this version>",
        "alternative_titles" : [<list of alternative titles>],
        "summary" : "<free text summary>",
        "language" : [<list of languages>],
        "singer" : "<opaque identifier of the singer>",
        "collector" : "<free text name of collector>",
        "source" : "<free text source of material>",
        "collected_date" : "<datestamp of collection>",
        "location" : [
            {
                "relation" : "<nature of song's relationship to place>",
                "lat" : "<latitude>",
                "long" : "<longitude>",
                "name" : "<textual name of place>"
            }
        ],
        "references" : [
            {
                "type" : "<reference type, e.g. ROUD>",
                "number" : "<reference number>"
            }
        ],
        "comments" : "<free text comments>",
        "tags" : [<list of tags>],
        "created_date" : "<created date>",
        "last_updated" : "<last updated date>"
    }

* id - the opaque system identifier for the version; not for use by the outside world
* lv_id - The Local Voices identifier for the version
* title - this is the name of this version of the song
* alternative_titles - any alternative titles for this version of the song
* language - one of English, Scots, Gaelic, Other
* location - a list of locations relevant to the version.  Each location is a compound attribute with the lat/long and the name of the place, as well as an optional relationship the place has to the version
* references - other numbering or classification schemes for this version (e.g. the ROUD number)
* comments - free text comments on the version
* tags - tags associated with the version
* created_date - a timestamp, system assigned, for the moment the record was created
* last_updated - a timestamp, system assigned, for the last time the record was updated

## Data Store

Data Storage will be provided entirely in Elasticsearch, but we will use part of the index like a relational data store for convenience, and construct searchable indices for the various datatypes from that relational store.

### Relational Model

6 datatypes are required to model the content:

1. Song Store - metadata for the song
2. Version Store - metadata for the version
3. Singer Store - metadata for the singer
4. Song2Version - link table from Songs to Versions
5. Singer2Version - link table from Singers to Versions
6. Song2Song - link table from Songs to other Songs

#### Song Store

Documents held in the Song Store will have the following form:

    {
        "id" : "<opaque internal identifier>",
        "lv_id" : "<local voices identifier>",
        "title" : "<canonical song title>",
        "summary" : "<free text summary>",
        "location": [
            {
                "relation" : "<nature of song's relationship to place>",
                "lat" : "<latitude>",
                "long" : "<longitude>",
                "name" : "<textual name of place>"
            }
        ],
        "time_period" : {
            "from" : "<partial date>",
            "to" : "<partial date>"
        },
        "composer" : "<free text name of composer>",
        "created_date" : "<created date>",
        "last_updated" : "<last updated date>"
    }

#### Version Store

Documents held in the Version Store will have the following form:

    {
        "id" : "<opaque internal identifier>",
        "lv_id" : "<local voices identifier>",
        "title" : "<title of this version>",
        "alternative_titles" : [<list of alternative titles>],
        "summary" : "<free text summary>",
        "language" : [<list of languages>],
        "collector" : "<free text name of collector>",
        "source" : "<free text source of material>",
        "collected_date" : "<datestamp of collection>",
        "location" : [
            {
                "relation" : "<nature of song's relationship to place>",
                "lat" : "<latitude>",
                "long" : "<longitude>",
                "name" : "<textual name of place>"
            }
        ],
        "references" : [
            {
                "type" : "<reference type, e.g. ROUD>",
                "number" : "<reference number>"
            }
        ],
        "comments" : "<free text comments>",
        "tags" : [<list of tags>],
        "created_date" : "<created date>",
        "last_updated" : "<last updated date>"
    }

#### Singer Store

Documents held in the Singer Store will have the following form:

    {
        "id" : "<opaque internal identifier>",
        "lv_id" : "<local voices identifier>",
        "name" : {
            "first" : "<first name>",
            "middle" : "<middle name or initial>",
            "last" : "<surname>",
            "aka" : [<nicknames and translations>]
        },
        "groups" : [<list of bands/choirs>],
        "gender" : "<male|female>",
        "location" : [
            {
                "relation" : "<nature of singers relationship to place>",
                "lat" : "<latitude>",
                "long" : "<longitude>",
                "name" : "<textual name of place>"
            }
        ]
        "born" : "<(partial) datestamp>",
        "died" : "<(partial) datestamp>",
        "biography" : "<biographical summary>"
        "created_date" : "<created date>",
        "last_updated" : "<last updated date>"
    }

#### Song2Version

Documents held in the Song2Version link table will have the following form:

    {
        "id" : "<opaque internal identifier>",
        "song_id" : "<opaque identifier for the song>",
        "version_id" : "<opaque identifier for the version>",
        "created_date" : "<date this relationship was created>"
    }


#### Singer2Version

Documents held in the Singer2Version link table will have the following form:

    {
        "id" : "<opaque internal identifier>",
        "singer_id" : "<opaque identifier for the singer>",
        "version_id" : "<opaque identifier for the version>",
        "created_date" : "<date this relationship was created>"
    }

#### Song2Song

Documents held in the Song2Song link table will have the following form:

    {
        "id" : "<opaque internal identifier>",
        "song_id_1" : "<opaque identifier for the second song>",
        "song_id_2" : "<opaque identifier for the second song>",
        "created_date" : "<date this relationship was created>"
    }

### Index Model

3 indices are required to service the various search requirements

1. Song Index - metadata for the song, embedded list of versions with embedded singers
2. Singer Index - metadata for the singer, embedded list of versions
3. Version Index - metadata for the version and metadata for the singer and relationship to the song

#### Song Index

    {
        "id" : "<opaque internal identifier>",
        "lv_id" : "<local voices identifier>",
        "title" : "<canonical song title>",
        "summary" : "<free text summary>",
        "location": [
            {
                "relation" : "<nature of song's relationship to place>",
                "lat" : "<latitude>",
                "long" : "<longitude>",
                "name" : "<textual name of place>"
            }
        ],
        "time_period" : {
            "from" : "<partial date>",
            "to" : "<partial date>"
        },
        "composer" : "<free text name of composer>",
        "created_date" : "<created date>",
        "last_updated" : "<last updated date>",
        
        "canonical_location" : {
            "lat" : "<canonical latitude for the song>",
            "lon" : "<canonical longitude for the song>",
        },
        "alternative_titles" : [<list of alternative song titles>],
        "relations" : [
            {
                "id" : "<opaque identifier for related song>",
                "title" : "<canonical title of related song>"
            }
        ],
        "references" : [
            {
                "type" : "<reference type, e.g. ROUD>",
                "number" : "<reference number>"
            }
        ],
        "versions" : [
            {
                "id" : "<opaque internal identifier>",
                "lv_id" : "<local voices identifier>",
                "title" : "<title of this version>",
                "alternative_titles" : [<list of alternative titles>],
                "summary" : "<free text summary>",
                "language" : [<list of languages>],
                "collector" : "<free text name of collector>",
                "source" : "<free text source of material>",
                "collected_date" : "<datestamp of collection>",
                "location" : [
                    {
                        "relation" : "<nature of song's relationship to place>",
                        "lat" : "<latitude>",
                        "long" : "<longitude>",
                        "name" : "<textual name of place>"
                    }
                ],
                "references" : [
                    {
                        "type" : "<reference type, e.g. ROUD>",
                        "number" : "<reference number>"
                    }
                ],
                "comments" : "<free text comments>",
                "tags" : [<list of tags>],
                "created_date" : "<created date>",
                "last_updated" : "<last updated date>",
                
                "canonical_location" : {
                    "lat" : "<canonical latitude for the singer>",
                    "lon" : "<canonical longitude for the singer>",
                },
                "singer" : {
                    "id" : "<opaque internal identifier>",
                    "lv_id" : "<local voices identifier>",
                    "name" : {
                        "first" : "<first name>",
                        "middle" : "<middle name or initial>",
                        "last" : "<surname>",
                        "aka" : [<nicknames and translations>]
                    },
                    "groups" : [<list of bands/choirs>],
                    "gender" : "<male|female>",
                    "location" : [
                        {
                            "relation" : "<nature of singers relationship to place>",
                            "lat" : "<latitude>",
                            "long" : "<longitude>",
                            "name" : "<textual name of place>"
                        }
                    ]
                    "born" : "<(partial) datestamp>",
                    "died" : "<(partial) datestamp>",
                    "biography" : "<biographical summary>"
                    "created_date" : "<created date>",
                    "last_updated" : "<last updated date>",
                    
                    "canonical_location" : {
                        "lat" : "<canonical latitude for the singer>",
                        "lon" : "<canonical longitude for the singer>",
                    },
                    "born_date" : "<full datestamp>",
                    "died_date" : "<full datestamp>"
                }
            }
        ]
    }

* canonical_location - canonical lat/long to be used for geographical queries.  These will require ES type "geo_point"
* alternative_titles - these are computed from the version titles and alternative titles
* relations - these are songs which are related in some way to the current song.  We just include their title and their id, for convenience in display
* references - aggregate of reference numbers computed from the version references
* versions - a list of all of the song versions, computed from Song2Version, with each version containing an embedded singer, computed from Singer2Version.  Note that this versions object is _almost_ identical to the individual versions objects in the Versions Index
    * In the "singer" field of the versions object we incorporate the canonical_location, born_date and died_date as simple computed fields
    * Note that we also incorporate the canonical_location field for the version itself, which is a simple computed field

### Singer Index

    {
        "id" : "<opaque internal identifier>",
        "lv_id" : "<local voices identifier>",
        "name" : {
            "first" : "<first name>",
            "middle" : "<middle name or initial>",
            "last" : "<surname>",
            "aka" : [<nicknames and translations>]
        },
        "groups" : [<list of bands/choirs>],
        "gender" : "<male|female>",
        "location" : [
            {
                "relation" : "<nature of singers relationship to place>",
                "lat" : "<latitude>",
                "long" : "<longitude>",
                "name" : "<textual name of place>"
            }
        ]
        "born" : "<(partial) datestamp>",
        "died" : "<(partial) datestamp>",
        "biography" : "<biographical summary>",
        "created_date" : "<created date>",
        "last_updated" : "<last updated date>",
        
        "canonical_location" : {
            "lat" : "<canonical latitude for the singer>",
            "lon" : "<canonical longitude for the singer>",
        },
        "born_date" : "<full datestamp>",
        "died_date" : "<full datestamp>",
        "versions" : [
            {
                "id" : "<opaque internal identifier>",
                "lv_id" : "<local voices identifier>",
                "title" : "<title of this version>",
                "alternative_titles" : [<list of alternative titles>],
                "summary" : "<free text summary>",
                "language" : [<list of languages>],
                "collector" : "<free text name of collector>",
                "source" : "<free text source of material>",
                "collected_date" : "<datestamp of collection>",
                "location" : [
                    {
                        "relation" : "<nature of song's relationship to place>",
                        "lat" : "<latitude>",
                        "long" : "<longitude>",
                        "name" : "<textual name of place>"
                    }
                ],
                "references" : [
                    {
                        "type" : "<reference type, e.g. ROUD>",
                        "number" : "<reference number>"
                    }
                ],
                "comments" : "<free text comments>",
                "tags" : [<list of tags>],
                "created_date" : "<created date>",
                "last_updated" : "<last updated date>",
                
                "canonical_location" : {
                    "lat" : "<canonical latitude for the singer>",
                    "lon" : "<canonical longitude for the singer>",
                },
                "song" : {
                    "id" : "<opaque internal identifier>",
                    "lv_id" : "<local voices identifier>",
                    "title" : "<canonical song title>",
                    "summary" : "<free text summary>",
                    "location": [
                        {
                            "relation" : "<nature of song's relationship to place>",
                            "lat" : "<latitude>",
                            "long" : "<longitude>",
                            "name" : "<textual name of place>"
                        }
                    ],
                    "time_period" : {
                        "from" : "<partial date>",
                        "to" : "<partial date>"
                    },
                    "composer" : "<free text name of composer>",
                    "created_date" : "<created date>",
                    "last_updated" : "<last updated date>",
                    
                    "canonical_location" : {
                        "lat" : "<canonical latitude for the song>",
                        "lon" : "<canonical longitude for the song>",
                    },
                    "alternative_titles" : [<list of alternative song titles>]
                }
            }
        ]
    }

* canonical_location - canonical lat/long to be used for geographical queries.  These will require ES type "geo_point"
* born_date - full datestamp computed from the partial datestamp in "born" (e.g. if born says "1975", born_date says "01-01-1975")
* died_date - full datestamp computed from the partial datestamp in "died" (e.g. if died says "1975", died_date says "01-01-1975")
* versions - a list of all of the song versions, computed from Singer2Version, with each version containing an embedded song, computed from Song2Version.  Note that this versions object is _almost_ identical to the individual versions objects in the Versions Index
    * Note that in the "song" field in the version object, we incorporate the canonical_location and the alternative_titles as simple computed fields.  We do not incorporate the more complex computed fields, as these are unnecessary for searching on this object.
    * Note that we also incorporate the canonical_location field in the version itself, as a simple computed field

#### Versions Index

    {
        "id" : "<opaque internal identifier>",
        "lv_id" : "<local voices identifier>",
        "title" : "<title of this version>",
        "alternative_titles" : [<list of alternative titles>],
        "summary" : "<free text summary>",
        "language" : [<list of languages>],
        "collector" : "<free text name of collector>",
        "source" : "<free text source of material>",
        "collected_date" : "<datestamp of collection>",
        "location" : [
            {
                "relation" : "<nature of song's relationship to place>",
                "lat" : "<latitude>",
                "long" : "<longitude>",
                "name" : "<textual name of place>"
            }
        ],
        "references" : [
            {
                "type" : "<reference type, e.g. ROUD>",
                "number" : "<reference number>"
            }
        ],
        "comments" : "<free text comments>",
        "tags" : [<list of tags>],
        "created_date" : "<created date>",
        "last_updated" : "<last updated date>",
        
        "canonical_location" : {
            "lat" : "<canonical latitude for the singer>",
            "lon" : "<canonical longitude for the singer>",
        },
        "singer" : {
            "id" : "<opaque internal identifier>",
            "lv_id" : "<local voices identifier>",
            "name" : {
                "first" : "<first name>",
                "middle" : "<middle name or initial>",
                "last" : "<surname>",
                "aka" : [<nicknames and translations>]
            },
            "groups" : [<list of bands/choirs>],
            "gender" : "<male|female>",
            "location" : [
                {
                    "relation" : "<nature of singers relationship to place>",
                    "lat" : "<latitude>",
                    "long" : "<longitude>",
                    "name" : "<textual name of place>"
                }
            ]
            "born" : "<(partial) datestamp>",
            "died" : "<(partial) datestamp>",
            "biography" : "<biographical summary>"
            "created_date" : "<created date>",
            "last_updated" : "<last updated date>",
            
            "canonical_location" : {
                "lat" : "<canonical latitude for the singer>",
                "lon" : "<canonical longitude for the singer>",
            },
            "born_date" : "<full datestamp>",
            "died_date" : "<full datestamp>",
        },
        "song" : {
            "id" : "<opaque internal identifier>",
            "lv_id" : "<local voices identifier>",
            "title" : "<canonical song title>",
            "summary" : "<free text summary>",
            "location": [
                {
                    "relation" : "<nature of song's relationship to place>",
                    "lat" : "<latitude>",
                    "long" : "<longitude>",
                    "name" : "<textual name of place>"
                }
            ],
            "time_period" : {
                "from" : "<partial date>",
                "to" : "<partial date>"
            },
            "composer" : "<free text name of composer>",
            "created_date" : "<created date>",
            "last_updated" : "<last updated date>",
            
            "canonical_location" : {
                "lat" : "<canonical latitude for the song>",
                "lon" : "<canonical longitude for the song>",
            },
            "alternative_titles" : [<list of alternative song titles>]
        }
    }

* canonical_location - canonical lat/long to be used for geographical queries.  These will require ES type "geo_point"
* singer - record for the singer of this version of the song. Note that we incorporate the canonical_location, born_date and died_date as simple computed fields
* song - record for the song this is a version of.  Note that we incorporate the canonical_location and the alternative_titles as simple computed fields.  We do not incorporate the more complex computed fields, as these are unnecessary for searching on this object.

### Storage Process

**1/ Add or update a song**

1. Add the song to the Song Store
2. Compute any new relations to versions and any removed relationships.  New relations should be added to Song2Version, redundant relationships should be removed
2. Compute any new relations to other songs and any removed relationships.  New relations should be added to Song2Song, redundant relationships should be removed
4. Regenerate the Song Index for this song
5. Regenerate the Song Index for all songs whose relationships were affected
6. Regenerate the Version Index for all versions whose relationships were affected

**2/ Add or update a singer**

1. Add the singer to the Singer Store
2. Compute any new relations to versions and any removed relationships.  New relations should be added to Singer2Version, redundant relationships should be removed
3. Regenerate the Singer Index for this singer
4. For each version referenced by the singer record, regenerate the Version Index

**3/ Add or update a version**

1. Add the version to the Version Store
2. Compute any new relations to songs and any removed relationships.  New relations should be added to Song2Version, redundant relationships should be removed
3. Compute any new relations to singers and any removed relationships.  New relations should be added to Singer2Version, redundant relationships should be removed
4. Regenerate the Version Index for this version
5. Regenerate the Song Index for the related song
6. Regenerate the Singer Index for the related singer

**4/ Delete a song**

1. Delete all the relations from Song2Version
2. Delete the song from the Song Store
3. Delete the song from the Song Index
4. For each version, delete the version as per (6)

**5/ Delete a singer**

1. Delete all the relations from Singer2Version
2. Delete the singer from the Singer Store
3. Delete the singer from the Singer Index
4. Update the Version Index for the affected version
5. Update the Song Index for the song to which the version is related

**6/ Delete a version**

1. Delete all the relations from Song2Version
2. Delete all the relations from Singer2Version
3. Delete the version from the Version Store
4. Delete the version from the Version Index
5. Update the Singer Index for the affected singer
6. Update the Song Index for the affected song


## API

### Search and Retrieve API

**1/ Provide the main search API which satisfies search scenarios (1), (2) and (5) above**

    GET /search?<params>

The following URL params are permitted

* from_lat - upper-most latitude for search results
* to_lat - lower-most latitude for search results
* from_long - left-most longitude for search results
* to_long - right-most longitude for search results
* place - placename to search for
* q - free-text query string
* type - one or more of "singer", "song", "version" as a comma-delimitted list

This returns simple, minimal JSON representations of the objects that match

**2/ Retrieve full details about a singer**

    GET /singer/<id>

* id - the system's internal identifier for the singer

This returns a full JSON representation of the singer, including all of the song variations they are responsible for

**3/ Retrieve full details about a song**

    GET /song/<id>
    
* id - the system's internal identifier for the song

This returns a full JSON representation of the song, including all of the song variations

**4/ List the singers alphabetically**

    GET /singers?<params>

The following URL params are permitted:

* from - the result number to commence listing from.  Defaults to 0, and is used for result set paging
* size - the size of the result set, and can be used to determine the "from" value for the next request when paging
* letter - the specific letter the singer's name should start with

Returns a JSON list of names and singer ids in alphabetical order

### Auto-Complete API

NOTE: this will only be developed if there is sufficient time

    GET /ac/<field>?q=<search>

<search> is the substring of the value to be autocompleted

The field can be one of the following:

* place - returns a list of placenames
* composer - returns list of composers that have previously been entered into the system
* tag - returns a list of tags that have previously been entered into the system

### Create/Update/Delete API

**1/ Create a new singer**

    POST /singers 
    <JSON representation of singer>

Returns the internal identifier of the singer created

**2/ Update an existing singer**

    PUT /singer/<id>
    <JSON representation of singer>
    
* id - the internal identifier of the singer (as returned by the POST operation)

Does not return anything

**3/ Delete a singer**

NOTE: delete is quite destructive - we may choose to provide only soft-delete at this stage, or to omit delete altogether

    DELETE /singer/</id>

* id - the internal identifier of the singer (as returned by the POST operation)

Does not return anything

NOTE: delete of a singer will result in the delete of all the versions associated with that singer

**4/ Create a new song**

    POST /songs 
    <JSON representation of song>

Returns the internal identifier of the song created

**5/ Update an existing singer**

    PUT /song/<id>
    <JSON representation of song>
    
* id - the internal identifier of the song (as returned by the POST operation)

Does not return anything

**6/ Delete a song**

NOTE: delete is quite destructive - we may choose to provide only soft-delete at this stage, or to omit delete altogether

    DELETE /song/</id>

* id - the internal identifier of the song (as returned by the POST operation)

Does not return anything

NOTE: delete of a song will result in the delete of all the versions associated with that song

**7/ Create a new version**

    POST /versions 
    <JSON representation of version>

Returns the internal identifier of the version created

**8/ Update an existing version**

    PUT /version/<id>
    <JSON representation of version>
    
* id - the internal identifier of the version (as returned by the POST operation)

Does not return anything

**9/ Delete a version**

NOTE: delete is quite destructive - we may choose to provide only soft-delete at this stage, or to omit delete altogether

    DELETE /version/</id>

* id - the internal identifier of the version (as returned by the POST operation)

Does not return anything


## Resources

Geocoding:
http://en.wikipedia.org/wiki/List_of_United_Kingdom_locations
http://www.gazetteer.org.uk/purchase.php
http://www.svincent.com/CrystalObelisk/Names/towns.txt
http://www.nearby.org.uk/
https://developers.google.com/maps/documentation/geocoding/

Relational data in ES:
http://www.elasticsearch.org/blog/managing-relations-inside-elasticsearch/
