#!/usr/bin/env python3
"""
Script para actualizar las canciones del EP con los enlaces específicos de Spotify
"""

import json

def update_ep_songs():
    """
    Actualiza las canciones del EP con los enlaces específicos de Spotify
    """
    
    # Leer el archivo actual
    with open('data/music/discography.json', 'r', encoding='utf-8') as f:
        discography = json.load(f)
    
    # Nuevas canciones del EP con enlaces específicos
    ep_songs = [
        {
            "title": "Me Lleve a la Luna",
            "plays": 250000,
            "year": 2025,
            "spotify_url": "https://open.spotify.com/intl-es/track/0x3jIl43Ch2b2F9eflP6Oh",
            "album": "Me Lleve a la Luna",
            "image_url": "data/media/covers/pepito-grillo-ep-cover.png",
            "duration": "3:06"
        },
        {
            "title": "Vuelvo al Pueblo",
            "plays": 200000,
            "year": 2025,
            "spotify_url": "https://open.spotify.com/intl-es/track/1CrPXxbLIP4PabXzoxm8rN",
            "album": "Me Lleve a la Luna",
            "image_url": "data/media/covers/pepito-grillo-ep-cover.png",
            "duration": "3:18"
        },
        {
            "title": "Pepito Grillo",
            "plays": 180000,
            "year": 2025,
            "spotify_url": "https://open.spotify.com/intl-es/track/1FUNqepb8iEnG910CaS2a6",
            "album": "Me Lleve a la Luna",
            "image_url": "data/media/covers/pepito-grillo-ep-cover.png",
            "duration": "4:03",
            "featured_artist": "Miguelichi López"
        },
        {
            "title": "Tal Vez Fuimos",
            "plays": 160000,
            "year": 2025,
            "spotify_url": "https://open.spotify.com/intl-es/track/7Ll3GuLyz5whShM8nL7MbL",
            "album": "Me Lleve a la Luna",
            "image_url": "data/media/covers/pepito-grillo-ep-cover.png",
            "duration": "2:54"
        },
        {
            "title": "Sigo Sin Dormir",
            "plays": 150000,
            "year": 2025,
            "spotify_url": "https://open.spotify.com/intl-es/track/21BMN2tZ1cUG18dgaFgLnl",
            "album": "Me Lleve a la Luna",
            "image_url": "data/media/covers/pepito-grillo-ep-cover.png",
            "duration": "3:30"
        },
        {
            "title": "No Me Olvido",
            "plays": 140000,
            "year": 2025,
            "spotify_url": "https://open.spotify.com/intl-es/track/5mCTnACGQHUeYZYqOtKSAm",
            "album": "Me Lleve a la Luna",
            "image_url": "data/media/covers/pepito-grillo-ep-cover.png",
            "duration": "2:55",
            "featured_artist": "Muerdo"
        }
    ]
    
    # Mantener las otras canciones populares que no son del EP
    other_songs = [
        {
            "title": "Díselo a la Vida",
            "plays": 3299156,
            "year": 2020,
            "spotify_url": "https://open.spotify.com/intl-es/track/3fuX1oR1uI85OLm62Sbhej",
            "album": "Díselo a la Vida",
            "image_url": "https://image-cdn-fa.spotifycdn.com/image/ab67616d00001e02e2c21f9976cb66ab4700f0e1"
        },
        {
            "title": "Queremos Bailar",
            "plays": 1903496,
            "year": 2021,
            "spotify_url": "https://open.spotify.com/intl-es/track/0Roxgqo04t3AwYqmyy8P6x",
            "album": "Queremos Bailar",
            "image_url": "https://image-cdn-fa.spotifycdn.com/image/ab67616d00001e0200eb2057ef75bb2422bc1664"
        },
        {
            "title": "Mala Costumbre",
            "plays": 474353,
            "year": 2023,
            "spotify_url": "https://open.spotify.com/intl-es/track/5LqAuIpDtgawmL1ZaIF0I1",
            "album": "Mala Costumbre",
            "image_url": "https://image-cdn-ak.spotifycdn.com/image/ab67616d00001e021e1c761ad312d9518732375d"
        },
        {
            "title": "Color Esperanza",
            "plays": 110770,
            "year": 2020,
            "spotify_url": "https://open.spotify.com/intl-es/track/5y2rzbhfR057zhu0e9dIGh",
            "album": "OT Gala 6 (Operación Triunfo 2020)",
            "image_url": "https://image-cdn-fa.spotifycdn.com/image/ab67616d00001e029656f60161603bc70cdeb970"
        },
        {
            "title": "Alegría",
            "plays": 52753,
            "year": 2025,
            "spotify_url": "https://open.spotify.com/track/3K7XqX7vXH2c4Wx0t8Y5Y8",
            "album": "Alegría",
            "image_url": "https://image-cdn-ak.spotifycdn.com/image/ab67616d00001e02d6d22aae294ea5e9f7a7ed38"
        }
    ]
    
    # Combinar las canciones del EP con las otras canciones populares
    discography["popular_songs"] = ep_songs + other_songs
    
    # Actualizar la información del álbum EP
    for album in discography["albums"]:
        if album["title"] == "Me Lleve a la Luna":
            album["image_url"] = "data/media/covers/pepito-grillo-ep-cover.png"
            break
    
    # Guardar el archivo actualizado
    with open('data/music/discography.json', 'w', encoding='utf-8') as f:
        json.dump(discography, f, indent=4, ensure_ascii=False)
    
    print("✅ Canciones del EP actualizadas:")
    for song in ep_songs:
        print(f"   🎵 {song['title']} - {song['duration']}")
        if 'featured_artist' in song:
            print(f"      (con {song['featured_artist']})")
        print(f"      🔗 {song['spotify_url']}")
    
    return ep_songs

if __name__ == "__main__":
    update_ep_songs()
