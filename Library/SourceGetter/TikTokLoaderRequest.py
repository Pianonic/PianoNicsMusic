import requests
from bs4 import BeautifulSoup

class Data:
    def __init__(self, link, song_name, author, image):
        self.link = link
        self.song_name = song_name
        self.author = author
        self.image = image

async def GetTTLink(downloadURL):
    requestURL = "https://tmate.cc"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(requestURL, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    sessionToken = response.cookies.get("session_data")
    token = soup.find('input', {'name': 'token'})['value']

    requestURL = "https://tmate.cc/action"

    headers = {
        "cookie": f"session_data={sessionToken}",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    payload = {'url': downloadURL, 'token': token}
    
    response = requests.post(requestURL, data=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        
        key_value = data['data']
        
        soup = BeautifulSoup(key_value, 'html.parser')

        title = soup.find('h1').text.strip()
        author = soup.find('p').text.strip()
        image_url = soup.find('img')['src']
        download_links = soup.find_all('a', href=True)
        download_link = download_links[0]['href']

        print("Title:", title)
        print("Author:", author)
        print("Image URL:", image_url)
        print("Link:", download_link)
    else:
        print("Error:", response.status_code)

    return Data(link=download_link, song_name=title, author=author, image=image_url)
  
#GetTTLink("https://www.tiktok.com/@aydenmekus/video/7214283304256818478?is_from_webapp=1&sender_device=pc&web_id=7348931770685228576")