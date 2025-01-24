import os
import requests
from bs4 import BeautifulSoup
from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

url = "https://baomoi.com/"
cwd = os.path.dirname(__file__)
path = os.path.join(cwd, "output.txt")

def Output_Web_Scraping(content):
    with open(path, "a", encoding='utf-8') as output_file:
        output_file.writelines(content)
def ResetOutputFile():
    with open(path, "w", encoding="utf-8") as file:
        file.write("")

def Convert_File_Output():
    with open(path,"r", encoding='utf-8') as file:
        lines = file.readlines()
        return '\n'.join(lines)

def Scrape_News():
    ResetOutputFile()
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', target="_blank")
        prev = None
        for index, link in enumerate(links, start=1):
            title = link.get('title')
            if prev != title:
                Output_Web_Scraping(f"{index}. {title}: https://baomoi.com{link.get('href')}\n")
                prev = title    
    else:
        print(f"Failed to fetch url - Status code: {response.status_code}")
        return "Failed to fetch url"

def Keyword():
    keyword = input("Input keyword for filter: ")
    return keyword


def AI_Prompt():
    keyword = Keyword()
    prompt = Convert_File_Output() + "From these news headlines filter headlines related to " + keyword + ". Keep the format of the input with new indexing from 1"
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content
Scrape_News()
print(AI_Prompt())