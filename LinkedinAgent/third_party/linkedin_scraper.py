import requests
from dotenv import load_dotenv
import os


def getLinkedinDetails(url: str):
    load_dotenv()
    headers = {"Authorization": "Bearer " + os.getenv("PROXY_CURL_API_KEY")}
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    response = requests.get(api_endpoint, params={"url": url}, headers=headers)
    data = response.json()
    print(data)
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", " ", None)
        and k not in ["people_also_viewd", "certifications"]
    }

    if data.get("groups"):
        for gr in data.get("groups"):
            gr.pop("profile_pic_url")
    return data


if __name__ == "__main__":
    getLinkedinDetails("https://www.linkedin.com/in/rajan-ranjan15/")
