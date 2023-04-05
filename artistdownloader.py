from spotdl import Spotdl
from spotdl import types
from spotdl import SpotifyClient
from spotdl import utils
from spotdl.types.artist import Artist
from spotdl.types.album import Album
import sys
import time
import os

# download all albums from an artist and neatly organize them in ~/Music/ArtistName/AlbumName
def main():
    if len(sys.argv) < 2:
        print("Usage: python artistdownloader.py artist_url")
        return
    # login to spotify
    # spotdl.utils.spotify.SpotifyError: Spotify client not created. Call SpotifyClient.init(client_id, client_secret, user_auth, cache_path, no_cache, open_browser) first.
    # load from
    client_id = utils.config.get_config()['client_id']
    client_secret = utils.config.get_config()['client_secret']
    spotdl = Spotdl(client_id, client_secret)
    #artist_search = Artist.search(sys.argv[1])
    #artist_url = artist_search['artists']['items'][0]['external_urls']['spotify']
    artist = Artist.from_url(sys.argv[1])
    print("Downloading all albums from " + artist.name)
    albumnames = []
    for album in artist.albums:
        current = Album.from_url(album)
        name = Album.get_metadata(album)[0]["name"]
        # skip duplicate albums
        if name in albumnames:
            continue
        if "deluxe" in name.lower() \
            or "bonus" in name.lower() \
            or "live" in name.lower() \
            or "version" in name.lower() \
            or "bundle" in name.lower() \
            or "single" in name.lower() \
            or "ep" in name.lower() \
            or "mix" in name.lower() \
            or "edit" in name.lower():
            continue
        albumnames.append(name)
        print("Downloading album: " + name)
        # create directory for album
        os.system("mkdir -p -v \"/home/kek/Music/" + artist.name + "/" + name + "\"")
        # change directory to album directory
        os.chdir("/home/kek/Music/" + artist.name + "/" + name)
        # download album via terminal command
        os.system("spotdl " + album)


if __name__ == '__main__':
    main()
