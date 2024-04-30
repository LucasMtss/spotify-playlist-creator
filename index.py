import spotipy
from spotipy.oauth2 import SpotifyOAuth

def search_artist(artist_name, sp):
    result = sp.search(q=artist_name, type='artist', limit=10)
    artists = result['artists']['items']
    return artists

def top_tracks(artist_id, sp):
    tracks = sp.artist_top_tracks(artist_id, country='BR')
    return tracks['tracks']

def create_playlist(playlist_name, track_uris, sp):
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user_id, playlist_name, public=False)
    playlist_id = playlist['id']
    sp.playlist_add_items(playlist_id, track_uris)

# Configuração da autenticação
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="", client_secret="", scope="playlist-modify-private", redirect_uri="http://localhost:3000"))

def select_artists():
    selected_artists = []
    while True:
        artist_name = input("Digite o nome do artista que deseja buscar (ou deixe em branco para terminar): ")
        if not artist_name:
            break
        artists = search_artist(artist_name, sp)
        if artists:
            print("Artistas encontrados:")
            for index, artist in enumerate(artists):
                print(f"{index+1}. {artist['name']}")
            artist_index = int(input("Digite o número do artista desejado: ")) - 1
            selected_artists.append(artists[artist_index])
        else:
            print("Artista não encontrado.")
    return selected_artists

def main():
    selected_artists = select_artists()

    if selected_artists:
        print("\nArtistas selecionados:")
        for artist in selected_artists:
            print(artist['name'])
        print("\n")

        all_tracks = []
        for artist in selected_artists:
            top_tracks_result = top_tracks(artist['id'], sp)
            if top_tracks_result:
                print(f"As 10 músicas mais tocadas de {artist['name']}:")
                for index, track in enumerate(top_tracks_result[:10]):
                    print(f"{index+1}. {track['name']}")
                all_tracks.extend(top_tracks_result[:10])

        create_playlist_input = input("\nDeseja criar uma playlist com estas músicas? (sim/não): ").lower()
        if create_playlist_input == "sim":
            playlist_name = input("Digite o nome da playlist: ")
            track_uris = [track['uri'] for track in all_tracks]
            create_playlist(playlist_name, track_uris, sp)
            print("Playlist criada com sucesso!")
        else:
            print("Operação cancelada.")

if __name__ == "__main__":
    main()
