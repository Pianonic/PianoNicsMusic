import requests

def fetch_choices():
    try:
        url = "http://localhost:7897/run/infer_refresh"
        response = requests.post(url, json={"data": []})
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        model_choices = [choice for choice in data["data"][0]["choices"]]
        index_choices = [choice.split("/")[-1] for choice in data["data"][1]["choices"]]
        return model_choices, index_choices
    except requests.exceptions.RequestException as e:
        print("Error generating AI vocals:", e)

def check_connection():
    try:
        url = "http://localhost:7897"
        response = requests.get(url)
        response.raise_for_status()
        return True
    except:
        print("Server is not running. Please start the AI server.")
        return False