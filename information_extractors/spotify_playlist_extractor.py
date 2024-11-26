import json
from spotapi import PublicPlaylist

publicPlaylist = PublicPlaylist("https://open.spotify.com/playlist/1CQQVPBBlpP03GkEVjyd33?si=e8423d3153b54ea0")
car = list(publicPlaylist.paginate_playlist())
var = publicPlaylist.get_playlist_info(limit=0)
playlist_name = publicPlaylist.name if hasattr(publicPlaylist, 'name') else "Unnamed_Playlist"
playlist_name_safe = var['data']['playlistV2']['name']
playlist_info = []

for paa in car:
    for item in paa.get("items", []):
        track = item.get("itemV2", {}).get("data", {})
        track_name = track.get("name")
        if track_name:
            # Attempt to decode using utf-8, ignoring errors if they occur
            track_name = track_name.encode('utf-8', 'ignore').decode('utf-8')
        artists = track.get("artists", {}).get("items", [])
        artist_names = [artist.get("profile", {}).get("name") for artist in artists if artist.get("profile", {}).get("name")]
        if track_name and artist_names:
            playlist_info.append({
                "track_name": track_name,
                "artist_names": artist_names
            })

output_data = {
    "songs": playlist_info,
    "total_entries": len(playlist_info)
}

output_filename = f"{playlist_name_safe}_songs_info.json"

with open(output_filename, 'w', encoding='utf-8') as json_file:
    json.dump(output_data, json_file, indent=4, ensure_ascii=False)

print(f"Data has been written to '{output_filename}'. Total entries: {len(playlist_info)}")
