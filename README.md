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
                "lon" : "<longitude>",
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
        "alternative_title" : [<list of alternative song titles>],
        "summary" : "<free text summary>",
        "location": [
            {
                "relation" : "<nature of song's relationship to place>",
                "lat" : "<latitude>",
                "lon" : "<longitude>",
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
* alternative_title - this is all of the titles of the song variants
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
        "alternative_title" : [<list of alternative titles>],
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
                "lon" : "<longitude>",
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
* alternative_title - any alternative titles for this version of the song
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
                "lon" : "<longitude>",
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
    }

#### Version Store

Documents held in the Version Store will have the following form:

    {
        "id" : "<opaque internal identifier>",
        "lv_id" : "<local voices identifier>",
        "title" : "<title of this version>",
        "alternative_title" : [<list of alternative titles>],
        "summary" : "<free text summary>",
        "language" : [<list of languages>],
        "collector" : "<free text name of collector>",
        "source" : "<free text source of material>",
        "collected_date" : "<datestamp of collection>",
        "location" : [
            {
                "relation" : "<nature of song's relationship to place>",
                "lat" : "<latitude>",
                "lon" : "<longitude>",
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
                "lon" : "<longitude>",
                "name" : "<textual name of place>"
            }
        ]
        "born" : "<(partial) datestamp>",
        "died" : "<(partial) datestamp>",
        "biography" : "<biographical summary>"
        "created_date" : "<created date>",
        "last_updated" : "<last updated date>",
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
        "song_ids" : [
            "<opaque identifier for the second song>",
            "<opaque identifier for the first song>"
        ]
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
                "lon" : "<longitude>",
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
        "alternative_title" : [<list of alternative song titles>],
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
                "alternative_title" : [<list of alternative titles>],
                "summary" : "<free text summary>",
                "language" : [<list of languages>],
                "collector" : "<free text name of collector>",
                "source" : "<free text source of material>",
                "collected_date" : "<datestamp of collection>",
                "location" : [
                    {
                        "relation" : "<nature of song's relationship to place>",
                        "lat" : "<latitude>",
                        "lon" : "<longitude>",
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
                            "lon" : "<longitude>",
                            "name" : "<textual name of place>"
                        }
                    ]
                    "born" : "<(partial) datestamp>",
                    "died" : "<(partial) datestamp>",
                    "biography" : "<biographical summary>"
                    "created_date" : "<created date>",
                    "last_updated" : "<last updated date>",
                    
                    "canonical_name" : "<canonicalised version of the singer name>",
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
* alternative_title - these are computed from the version titles and alternative titles
* relations - these are songs which are related in some way to the current song.  We just include their title and their id, for convenience in display
* references - aggregate of reference numbers computed from the version references
* versions - a list of all of the song versions, computed from Song2Version, with each version containing an embedded singer, computed from Singer2Version.  Note that this versions object is _almost_ identical to the individual versions objects in the Versions Index
    * In the "singer" field of the versions object we incorporate the canonical_name, canonical_location, born_date and died_date as simple computed fields
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
                "lon" : "<longitude>",
                "name" : "<textual name of place>"
            }
        ]
        "born" : "<(partial) datestamp>",
        "died" : "<(partial) datestamp>",
        "biography" : "<biographical summary>",
        "created_date" : "<created date>",
        "last_updated" : "<last updated date>",
        
        "canonical_name" : "<canonicalised version of the singer name>",
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
                "alternative_title" : [<list of alternative titles>],
                "summary" : "<free text summary>",
                "language" : [<list of languages>],
                "collector" : "<free text name of collector>",
                "source" : "<free text source of material>",
                "collected_date" : "<datestamp of collection>",
                "location" : [
                    {
                        "relation" : "<nature of song's relationship to place>",
                        "lat" : "<latitude>",
                        "lon" : "<longitude>",
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
                            "lon" : "<longitude>",
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
                    "alternative_title" : [<list of alternative song titles>]
                }
            }
        ]
    }

* canonical_name - a human readable name computed from the compound "name" field
* canonical_location - canonical lat/long to be used for geographical queries.  These will require ES type "geo_point"
* born_date - full datestamp computed from the partial datestamp in "born" (e.g. if born says "1975", born_date says "01-01-1975")
* died_date - full datestamp computed from the partial datestamp in "died" (e.g. if died says "1975", died_date says "01-01-1975")
* versions - a list of all of the song versions, computed from Singer2Version, with each version containing an embedded song, computed from Song2Version.  Note that this versions object is _almost_ identical to the individual versions objects in the Versions Index
    * Note that in the "song" field in the version object, we incorporate the canonical_location and the alternative_title as simple computed fields.  We do not incorporate the more complex computed fields, as these are unnecessary for searching on this object.
    * Note that we also incorporate the canonical_location field in the version itself, as a simple computed field

#### Versions Index

    {
        "id" : "<opaque internal identifier>",
        "lv_id" : "<local voices identifier>",
        "title" : "<title of this version>",
        "alternative_title" : [<list of alternative titles>],
        "summary" : "<free text summary>",
        "language" : [<list of languages>],
        "collector" : "<free text name of collector>",
        "source" : "<free text source of material>",
        "collected_date" : "<datestamp of collection>",
        "location" : [
            {
                "relation" : "<nature of song's relationship to place>",
                "lat" : "<latitude>",
                "lon" : "<longitude>",
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
                    "lon" : "<longitude>",
                    "name" : "<textual name of place>"
                }
            ]
            "born" : "<(partial) datestamp>",
            "died" : "<(partial) datestamp>",
            "biography" : "<biographical summary>"
            "created_date" : "<created date>",
            "last_updated" : "<last updated date>",
            
            "canonical_name" : "<canonicalised version of the singer name>",
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
                    "lon" : "<longitude>",
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
            "alternative_title" : [<list of alternative song titles>]
        }
    }

* canonical_location - canonical lat/long to be used for geographical queries.  These will require ES type "geo_point"
* singer - record for the singer of this version of the song. Note that we incorporate the canonical_name, canonical_location, born_date and died_date as simple computed fields
* song - record for the song this is a version of.  Note that we incorporate the canonical_location and the alternative_title as simple computed fields.  We do not incorporate the more complex computed fields, as these are unnecessary for searching on this object.

### Storage Process

**1/ Add or update a song**

1. Add the song to the Song Store
2. Compute any new relations to versions and any removed relationships.  New relations should be added to Song2Version, redundant relationships should be removed
3. Compute any new relations to other songs and any removed relationships.  New relations should be added to Song2Song, redundant relationships should be removed
4. Regenerate the Song Index for this song
5. Regenerate the Song Index for all songs whose relationships were affected
6. Regenerate the Version Index for all versions whose relationships were affected
7. Regenerate the Singer Index for all singers whose versions were affected

**2/ Add or update a singer**

1. Add the singer to the Singer Store
2. Compute any new relations to versions and any removed relationships.  New relations should be added to Singer2Version, redundant relationships should be removed
3. Regenerate the Singer Index for this singer
4. For each version referenced by the singer record, regenerate the Version Index document
5. For each song associated with an affected version, regenerate the Song Index document

**3/ Add or update a version**

1. Add the version to the Version Store
2. Compute any new relations to songs and any removed relationships.  New relations should be added to Song2Version, redundant relationships should be removed
3. Compute any new relations to singers and any removed relationships.  New relations should be added to Singer2Version, redundant relationships should be removed
4. Regenerate the Version Index for this version
5. Regenerate the Song Index for the related song
6. Regenerate the Singer Index for the related singer

**4/ Delete a song**

1. Delete all the relations from Song2Version
2. Delete all the relations from Song2Song
3. Delete the song from the Song Store
4. Delete the song from the Song Index
5. For each related song, update the Song Index document
6. For each version, delete the version as per (6)

Note that deleting a song deletes all of the associated versions

**5/ Delete a singer**

1. Delete all the relations from Singer2Version
2. Delete the singer from the Singer Store
3. Delete the singer from the Singer Index
4. Update the Version Index for the affected version
5. Update the Song Index for the song to which the affected version is related

Note that deleting a singer does not delete the song versions

**6/ Delete a version**

1. Delete all the relations from Song2Version
2. Delete all the relations from Singer2Version
3. Delete the version from the Version Store
4. Delete the version from the Version Index
5. Update the Singer Index for the affected singer
6. Update the Song Index for the affected song (remember the Song may have been deleted as per (4))

## API

### Search and Retrieve API

**1/ Provide the main search API which satisfies search scenarios (1), (2) and (5) above**

    GET /search?<params>

The following URL params are permitted

* from_lat - upper-most latitude for search results
* to_lat - lower-most latitude for search results
* from_lon - left-most longitude for search results
* to_lon - right-most longitude for search results
* place - placename to search for
* q - free-text query string
* type - one or more of "singer", "song", "version" as a comma-delimitted list

This returns full JSON representations of the objects that match, as held in the index (not the store)

**2/ Retrieve full details about a singer**

    GET /singer/<id>

* id - the system's internal identifier for the singer

This returns a full JSON representation of the singer, including all of the song variations they are responsible for, as held in the index (not the store)

**3/ Retrieve full details about a song**

    GET /song/<id>
    
* id - the system's internal identifier for the song

This returns a full JSON representation of the song, including all of the song variations, as held in the index (not the store)

**4/ List the singers alphabetically**

    GET /singers?<params>

The following URL params are permitted:

* from - the result number to commence listing from.  Defaults to 0, and is used for result set paging
* size - the size of the result set, and can be used to determine the "from" value for the next request when paging
* letter - the specific letter the singer's name should start with

Returns a JSON list of names and singer ids in alphabetical order, with the count of the song versions associated

    [
        {
            "id" : "<opaque internal identifier for singer>",
            "name" : "<canonical version of singer's name>",
            "versions" : "<count of the number of song versions associated>"
        }
    ]

### Auto-Complete API

NOTE: this will only be developed if there is sufficient time

    GET /ac/<field>?q=<search>

<search> is the substring of the value to be autocompleted

The field can be one of the following:

* place - returns a list of placenames
* composer - returns list of composers that have previously been entered into the system
* tag - returns a list of tags that have previously been entered into the system

    [
        "<value1>",
        "<value2>",
        ...
    ]

### Create/Update/Delete API

**1/ Create a new singer**

_this operation also permits for the update of existing singers_

    POST /singers 
    <JSON representation of singer>

Returns the internal identifier of the singer created.

If the JSON representation of the singer contains an "id" field, then this will behave in the same way as (2).

The structure of the JSON representation is:

    {
        "id" : "<opaque singer identifier>",
        "singer" : {
            <singer object as per the storage model>
        },
        "versions" : [<list of opaque identifiers for versions>]
    }

* If the "id" field is provided, this will overwrite an existing record with the same identifier
* If the "singer" field is provided, then the singer metadata will be set as this metadata
* If the "versions" field is provided, then the singer will be related to the provided versions

Therefore, you may use this API request in the following ways:

1. Make a brand new singer, by just including the "singer" field
2. Overwrite an existing singer, by including the "id" and "singer" fields
3. Update an existing singer's versions by including the "id" and the "versions" fields
4. Create a new singer and immediately relate them to existing versions by including the "singer" and "versions" fields

**2/ Update an existing singer**

_that this API call is for REST-compliance, but the POST operation in (1) contains all the same functionality_

    PUT /singer/<id>
    <JSON representation of singer>
    
* id - the internal identifier of the singer (as returned by the POST operation)

Does not return anything

The structure of the JSON representation is:

    {
        "singer" : {
            <singer object as per the storage model>
        },
        "versions" : [<list of opaque identifiers for versions>]
    }

* If the "singer" field is provided, then the existing singer metadata will overwritten with this metadata
* If the "versions" field is provided, then the existing version relationships will be overwritten with these new ones

Therefore, you may use this API request in the following ways:

1. Overwrite an existing singer, by including "singer" field
2. Update an existing singer's versions by including "versions" field
3. Both of the above at the same time

**3/ Delete a singer**

_NOTE: delete is quite destructive - we may choose to provide only soft-delete at this stage, or to omit delete altogether_

    DELETE /singer/</id>

* id - the internal identifier of the singer (as returned by the POST operation)

Does not return anything

**4/ Create a new song**

_this operation also permits for the update of existing songs_

    POST /songs 
    <JSON representation of song>

Returns the internal identifier of the song created

If the JSON representation of the song contains an "id" field, then this will behave in the same way as (5).

The structure of the JSON representation is:

    {
        "id" : "<opaque song identifier>",
        "song" : {
            <song object as per the storage model>
        },
        "versions" : [<list of opaque identifiers for versions>],
        "songs" : [<list of opaque identifiers for other songs>]
    }

* If the "id" field is provided, this will overwrite an existing record with the same identifier
* If the "song" field is provided, then the song metadata will be set as this metadata
* If the "versions" field is provided, then the song will be related to the provided versions
* If the "songs" field is provided, then the song will be related to the provided songs

Therefore, you may use this API request in the following ways:

1. Make a brand new song, by just including the "singer" field
2. Overwrite an existing song, by including the "id" and "song" fields
3. Update an existing song's versions or related songs by including the "id" and/or the "versions"/"songs" fields
4. Create a new song and immediately relate them to existing versions and songs by including the "singer", "versions" and "songs" fields

**5/ Update an existing song**

_that this API call is for REST-compliance, but the POST operation in (4) contains all the same functionality_

    PUT /song/<id>
    <JSON representation of song>
    
* id - the internal identifier of the song (as returned by the POST operation)

Does not return anything

The structure of the JSON representation is:

    {
        "song" : {
            <song object as per the storage model>
        },
        "versions" : [<list of opaque identifiers for versions>],
        "songs" : [<list of opaque identifiers for other songs>]
    }

* If the "song" field is provided, then the song metadata will overwritten with this metadata
* If the "versions" field is provided, then any existing versions relationships will be overwritten with these new ones
* If the "songs" field is provided, then any existing song relationships will be overwritten with these new ones

Therefore, you may use this API request in the following ways:

1. Overwrite an existing song, by including "song" field
2. Update an existing songs's versions or related songs by including the "versions" and "songs" fields
3. Both of the above at the same time

**6/ Delete a song**

_NOTE: delete is quite destructive - we may choose to provide only soft-delete at this stage, or to omit delete altogether_

    DELETE /song/</id>

* id - the internal identifier of the song (as returned by the POST operation)

Does not return anything

NOTE: delete of a song will result in the delete of all the versions associated with that song

**7/ Create a new version**

_this operation also permits for the update of existing versions_

    POST /versions 
    <JSON representation of version>

Returns the internal identifier of the version created

If the JSON representation of the song contains an "id" field, then this will behave in the same way as (7).

The structure of the JSON representation is:

    {
        "id" : "<opaque version identifier>",
        "version : {
            <version object as per the storage model>
        },
        "song" : "<opaque identifier of song this is a version of>",
        "singer" : "<opaque identifier of singer this was performed by>"
    }

* If the "id" field is provided, this will overwrite an existing record with the same identifier
* If the "version" field is provided, then the version metadata will be set as this metadata
* If the "song" field is provided, then the version will be related to the provided song
* If the "singer" field is provided, then the version will be related to the provided singer

Therefore, you may use this API request in the following ways:

1. Make a brand new version, by just including the "version" field
2. Overwrite an existing version, by including the "id" and "version" fields
3. Update an existing version's song relationship or singer relationship by including the "id" and/or the "song"/"singer" fields
4. Create a new version and immediately relate it to an existing song and singer by including the "version", "song" and "singer" fields


**8/ Update an existing version**

_that this API call is for REST-compliance, but the POST operation in (7) contains all the same functionality_

    PUT /version/<id>
    <JSON representation of version>
    
* id - the internal identifier of the version (as returned by the POST operation)

Does not return anything

The structure of the JSON representation is:

    {
        "version : {
            <version object as per the storage model>
        },
        "song" : "<opaque identifier of song this is a version of>",
        "singer" : "<opaque identifier of singer this was performed by>"
    }

* If the "version" field is provided, then the version metadata will be overwritten with this metadata
* If the "song" field is provided, then the version will be related to the provided song
* If the "singer" field is provided, then the song will be related to the provided singer

Therefore, you may use this API request in the following ways:

1. Make a brand new version, by just including the "version" field
2. Overwrite an existing version, by including the "id" and "version" fields
3. Update an existing version's song relationship or singer relationship by including the "id" and/or the "song"/"singer" fields
4. Create a new version and immediately relate it to an existing song and singer by including the "version", "song" and "singer" fields

1. Overwrite an existing version, by including "version" field
2. Update an existing version's song or singer by including the "song" and "singer" fields
3. Both of the above at the same time

**9/ Delete a version**

_NOTE: delete is quite destructive - we may choose to provide only soft-delete at this stage, or to omit delete altogether_

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
