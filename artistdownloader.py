from spotdl import Spotdl
from spotdl import types
from spotdl import SpotifyClient
from spotdl import utils
import sys
import time
import os

# download all albums from an artist and neatly organize them in ~/Music/ArtistName/AlbumName
def main():
    if len(sys.argv) < 2:
        print("Usage: python artistdownloader.py artist")
        return
    # login to spotify
    # spotdl.utils.spotify.SpotifyError: Spotify client not created. Call SpotifyClient.init(client_id, client_secret, user_auth, cache_path, no_cache, open_browser) first.
    # load from
    client_id = utils.config.get_config()['client_id']
    client_secret = utils.config.get_config()['client_secret']
    spotdl = Spotdl(client_id, client_secret)
    artist_search = types.Artist.search(sys.argv[1])
    artist_url = artist_search['artists']['items'][0]['external_urls']['spotify']
    artist = types.Artist.from_url(artist_url)
    print("Downloading all albums from " + artist.name)
    albums = types.Artist.get_albums(artist_url)
    albumnames = []
    for album in albums:
        # skip duplicate albums
        if types.Album.get_metadata(album)['name'] in albumnames:
            continue
        if "deluxe" in types.Album.get_metadata(album)['name'].lower() \
            or "bonus" in types.Album.get_metadata(album)['name'].lower() \
            or "live" in types.Album.get_metadata(album)['name'].lower() \
            or "version" in types.Album.get_metadata(album)['name'].lower() \
            or "bundle" in types.Album.get_metadata(album)['name'].lower() \
            or "single" in types.Album.get_metadata(album)['name'].lower() \
            or "ep" in types.Album.get_metadata(album)['name'].lower() \
            or "mix" in types.Album.get_metadata(album)['name'].lower() \
            or "edit" in types.Album.get_metadata(album)['name'].lower():
            continue
        albumnames.append(types.Album.get_metadata(album)['name'])
        print("Downloading album: " + types.Album.get_metadata(album)['name'])
        # create directory for album
        os.system("mkdir -p -v \"/home/kek/Music/" + artist.name + "/" + types.Album.get_metadata(album)['name'] + "\"")
        # change directory to album directory
        os.chdir("/home/kek/Music/" + artist.name + "/" + types.Album.get_metadata(album)['name'])
        # download album via terminal command
        os.system("spotdl " + album)


if __name__ == '__main__':
    main()
