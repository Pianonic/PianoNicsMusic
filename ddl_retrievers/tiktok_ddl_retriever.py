import requests
from bs4 import BeautifulSoup
from models.music_information import MusicInformation

async def get_streaming_url(downloadURL):
    base_url = "https://tmate.cc"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Get session token
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    sessionToken = response.cookies.get("session_data")
    token = soup.find('input', {'name': 'token'})['value']

    # Make POST request
    action_url = f"{base_url}/action"
    headers["cookie"] = f"session_data={sessionToken}"
    payload = {'url': downloadURL, 'token': token}
    response = requests.post(action_url, data=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        key_value = data['data']
        soup = BeautifulSoup(key_value, 'html.parser')
        title = soup.find('h1').text.strip()
        author = soup.find('p').text.strip()
        image_url = soup.find('img')['src']
        download_links = soup.find_all('a', href=True)
        download_link = download_links[0]['href']
        return MusicInformation(streaming_url=download_link, song_name=title, author=author, image_url=image_url)
    else:
        return Exception("Error:", response.status_code)
