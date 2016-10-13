# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
from fixture import DataSet

class UserData(DataSet):
    class dartagnan:
        id = 1
        displayname = "D'Artagnan"
        username = 'darty'
        password = 'dart'
        email = 'dartagnan@mousquetaires.fr'
        shortBio = "Charles de Batz-Castelmore, Comte d'Artagnan (c. 1611 - 25 June 1673) served Louis XIV as captain of the Musketeers of the Guard"

    class athos:
        id = 2
        displayname = "Athos"
        username = 'athos'
        password = 'athos'
        email = 'athos@mousquetaires.fr'
        shortBio = "Athos (born c. 1580; died 1661) is a fictional character in the novels The Three Musketeers, Twenty Years After, and The Vicomte de Bragelonne by Alexandre Dumas, pure."

    class porthos:
        id = 3
        displayname = 'Porthos'
        username = "porthos"
        password = 'porthos'
        email = 'porthos@mousquetaires.fr'
        shortBio = "Porthos is a fictional character in the novels The Three Musketeers, Twenty Years After and The Vicomte de Bragelonne by Alexandre Dumas, pure."
    class aramis:
        id = 4
        displayname = 'Aramis esta re loco'
        username = "aramis"
        password = 'aramis'
        email = 'aramis@mousquetaires.fr'
        shortBio = "Rene d'Herblay 'Aramis' is a fictional character in the novels The Three Musketeers, Twenty Years After and The Vicomte de Bragelonne by Alexandre Dumas, pure."
    class phillipe:
        id = 5
        displayname = 'Phillipe'
        username = "phillipe"
        password = 'phillipe'
        email = 'phillipe@mousquetaires.fr'
        shortBio = "Phillipe is a fictional character created by Fernando Zunino for application testing purposes"
        
    class pepinot:
        id = 6
        displayname = 'Pepinot'
        username = "pepinot"
        password = 'pepinot'
        email = 'pepinot@choristes.fr'
        shortBio = "Pepinot is a fictional character from the movie Les Choristes"
        
    class john:
        id = 7
        displayname = 'John'
        username = "john"
        password = 'john'
        email = 'john@popego.com'
        shortBio = "John"
        

class ServiceTypeData(DataSet):
    class picture_service:
        id = 1
        type = 'photos'
        description = 'Photo sharing services (Flickr, PicasaWeb, etc)'
        is_media = True
    
    class video_service:
        id = 2
        type = 'videos'
        description = 'Video sharing services (YouTube, etc)'
        is_media = True

    class bookmark_service:
        id = 3
        type = 'bookmarks'
        description = 'bookmark sharing services (del.icio.us, stumbleupon, magnolia, etc)'
        is_media = True

    class music_service:
        id = 4
        type = 'music'
        description = 'last.fm thingies'
        is_media = True

class ServiceData(DataSet):
    class flickr:
        id = 1
        name = 'Flickr'
        description = 'Flickr is a thing where you upload your photos. OMFG!'
        url = 'http://www.flickr.com'
        agent = 'popserver.agents.flickr_agent:FlickrAgent()'
        type_id = ServiceTypeData.picture_service.ref('id')
        weight = 1

    class picasaweb:
        id = 2
        name = 'PicasaWeb'
        description = 'PicasaWEB is google\'s flickr'
        url = 'http://www.picasaweb.com'
        agent = 'popserver.agents.picasaweb_agent:PicasaWebAgent()'
        type_id = ServiceTypeData.picture_service.ref('id')
        weight = 1
    
    class youtube:
        id = 3
        name = 'YouTube'
        description = 'You Tube - Broadcast Yourself'
        url = 'http://www.youtube.com'
        agent = 'popserver.agents.youtube_agent'
        type_id = ServiceTypeData.music_service.ref('id')
        weight = 1

    class delicious:
        id = 4
        name = 'del.icio.us'
        description = 'del.icio.us is a place to store and share b00kmarkz'
        url = 'http://www.youtube.com'
        agent = 'popserver.agents.delicious_agent'
        type_id = ServiceTypeData.video_service.ref('id')
        weight = 1

    class lastfm:
        id = 5
        name = 'Last.FM'
        description = 'Last.FM is the posta'
        url = 'http://www.last.fm'
        agent = 'popserver.agents.lastfm_agent:LastFmAgent()'
        type_id = ServiceTypeData.music_service.ref('id')
        weight = 1

class VideoData(DataSet):
    class youtube_v1:
        id = 1
        external_id = 'yt_v1'
        title = 'title_yt_v1' 
        description ='video description 1'
        embedURL = "http://youtube.com/1/embed" 
        externalURL = "http://youtube.com/1/external" 
        service = ServiceData.youtube
        
    class youtube_v10:
        id = 10
        external_id = 'yt_v10'
        title = 'title_yt_v10' 
        description ='video description 10'
        embedURL = "http://youtube.com/10/embed" 
        externalURL = "http://youtube.com/10/external" 
        service = ServiceData.youtube
    class youtube_sin_description:
        id = 20
        external_id = 'yt_sin_description'
        title = 'title_yt_v10' 
        embedURL = "http://youtube.com/10/embed" 
        externalURL = "http://youtube.com/10/external" 
        service = ServiceData.youtube

class BookmarkData(DataSet):
    class slashdot:
        id = 2
        external_id = 'e3c52d69aa8ac9a7f421b3cca9a94436'
        title = 'Slashdot - News for nerds. Stuff that matters'
        description = 'nerdolandia'
        url = 'http://www.slashdot.org/'
        service = ServiceData.delicious
        serviceUrl = 'http://del.icio.us/url/slashdot'
        popularity = 100


    class kuro5hin:
        id = 3
        external_id = 'f1619ff2dfacfac3eb2e6132a5644205'
        title = 'Kuro5hin'
        description = 'technology and culture, from the trenches'
        url = 'http://www.kuro5hin.org/'
        service = ServiceData.delicious
        serviceUrl = 'http://del.icio.us/url/kuro5shin'
        popularity = 10


class ArtistData(DataSet):
    class queen:
        id = 100
        external_id = 'lfm_a1'
        title = 'title_lfm_a1' 
        description ='queen'
        service = ServiceData.lastfm


class SongData(DataSet):
    class killerQueen:
        id = 200
        external_id = 'lfm_s1'
        title = 'killer queen' 
        description ='killer queen descr'
        service = ServiceData.lastfm
        artist = ArtistData.queen

        
class UserItemData(DataSet):
    class phillipe_youtube_item1:
        id = 1
        item_id = VideoData.youtube_v1.ref('id')
        user = UserData.phillipe

    class darty_delicious_item1:
        id = 2
        item_id = BookmarkData.slashdot.ref('id')
        user = UserData.dartagnan

    class darty_delicious_item2:
        id = 3
        item_id = BookmarkData.kuro5hin.ref('id')
        user = UserData.dartagnan

    class aramis_delicious_item3:
        id = 4
        item_id = BookmarkData.slashdot.ref('id')
        user = UserData.aramis
        
    class pepinot_youtube_item10:
        id = 5
        item_id = VideoData.youtube_v10.ref('id')
        user = UserData.pepinot
        
    class pepinot_youtube_item1:
        id = 6
        item_id = VideoData.youtube_v1.ref('id')
        user = UserData.pepinot

class ArtistUserItemData(DataSet):
    class phillipe_lastfm_queen:
        id = 100
        item = ArtistData.queen
        user = UserData.phillipe
        play_count = 1


class SongUserItemData(DataSet):
    class phillipe_lastfm_killerQueen:
        id = 200
        item = SongData.killerQueen
        user = UserData.phillipe
        play_count = 1


class ItemGroupData(DataSet):
    class phillipe_youtube_favorites_group:
        id = 1
        name = 'favorites'
        external_id = 'yt_gr01'
        items = [UserItemData.phillipe_youtube_item1]

    class darty_delicious_group:
        id = 2
        name = 'Delicious Group'
        external_id = 'None'
        items = [UserItemData.darty_delicious_item1, UserItemData.darty_delicious_item2]

    class aramis_delicious_group:
        id = 3
        name = 'Delicious Group'
        external_id = 'None'
        items = [UserItemData.aramis_delicious_item3]
        
    class pepinot_youtube_favorites_group:
        id = 4
        name = 'pepinot favorites'
        external_id = 'yt_gr10'
        items = [UserItemData.pepinot_youtube_item10]
        
    class pepinot_youtube_myvideos_group:
        id = 5
        name = 'myvideos'
        external_id = 'yt_gr11'
        items = [UserItemData.pepinot_youtube_item1]

    class phillipe_lastfm_topartists_group:
        id = 6
        name = 'top artists'
        external_id = 'lfm_gr01'
        items = [ArtistUserItemData.phillipe_lastfm_queen]

    class phillipe_lastfm_topsongs_group:
        id = 7
        name = 'top songs'
        external_id = 'lfm_gr02'
        items = [SongUserItemData.phillipe_lastfm_killerQueen]
        
    
class TagData(DataSet):
    class foo:
        name = 'foo'
        items = [VideoData.youtube_v1]
        user_items = [UserItemData.darty_delicious_item1]
    class bar:
        name = 'bar'
        items = [VideoData.youtube_v1]
        user_items = [UserItemData.aramis_delicious_item3, UserItemData.phillipe_youtube_item1]
    class baz:
        name = 'baz'
        items = [VideoData.youtube_v1]
        
class AccountData(DataSet):
    class dartagnan_has_a_flickr_account:
        user = UserData.dartagnan
        service = ServiceData.flickr
        username = 'jazzido' # no cambiar, estoy usando mi cuenta de flickr en los tests

    class dartagnan_has_a_delicious_account:
        user = UserData.dartagnan
        service = ServiceData.delicious
        username = 'jazzido' # no cambiar, estoy usando mi cuenta de flickr en los tests
        item_groups = [ItemGroupData.darty_delicious_group]

    class dartagnan_has_a_lastfm_account:
        user = UserData.dartagnan
        service = ServiceData.lastfm
        username = 'maristaran' # no cambiar, estoy usando mi cuenta de flickr en los tests

    class aramis_has_a_picasa_account:
        user  = UserData.aramis
        service = ServiceData.picasaweb
        username = 'aramis'

    class aramis_has_a_delicious_account:
        user = UserData.aramis
        service = ServiceData.delicious
        username = 'aramis'
        item_groups = [ItemGroupData.aramis_delicious_group]
        
    class athos_has_a_youtube_account:
        user  = UserData.athos
        service = ServiceData.youtube
        username = 'nextuse'
        
    class phillipe_has_a_youtube_account:
        user  = UserData.phillipe
        service = ServiceData.youtube
        username = 'futureshorts'
        item_groups = [ItemGroupData.phillipe_youtube_favorites_group]        
    
    class pepinot_has_a_youtube_account:
        user  = UserData.pepinot
        service = ServiceData.youtube
        username = 'pepinot'
        item_groups = [ItemGroupData.pepinot_youtube_favorites_group, ItemGroupData.pepinot_youtube_myvideos_group]        
    
    class john_has_a_delicious_account:
        user  = UserData.john
        service = ServiceData.delicious
        username = 'john'        

    class phillipe_has_a_lastfm_account:
        user  = UserData.phillipe
        service = ServiceData.lastfm
        username = 'phillipemignon'
        item_groups = [ItemGroupData.phillipe_lastfm_topartists_group, ItemGroupData.phillipe_lastfm_topsongs_group]

    
class GlobalConfigData(DataSet):
    class tag_interest_threshold:
        property = 'interest.tagInterestThreshold'
        value = '4'

    class tag_interest_add_factor:
        property = 'interest.tagInterestAddFactor'
        value = '2'
