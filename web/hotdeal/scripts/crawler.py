from bs4 import BeautifulSoup
import requests
import telegram
from hotdeal.models import Deal
from datetime import datetime, timedelta

response = requests.get("https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu")
soup = BeautifulSoup(response.text, "html.parser")
BOT_TOKEN = "5727689894:AAEjmmryWcxGhAb7mQ8Lqe1IJjzlUQ81dR0"

bot = telegram.Bot(token=BOT_TOKEN)

def run():

    #delete deals order than 3days
    row, _ = Deal.objects.filter(created_at__lte=datetime.now() - timedelta(days=3)).delete()
    print(row, "deals deleted")
    for item in soup.find_all("tr", {"class" : ["list1", "list0"]}):
        try:
            img_src = item.find("img", class_ = "thumb_border").get("src")
            if img_src[:2] == "//":
                image = img_src[2:]
            else:
                image = img_src
            image = "http://" + image
            title = item.find("font", class_ = "list_title").text.strip()
            link = "https://www.ppomppu.co.kr" + item.find("a").get('href')
            reply_count = int(item.find("span", class_ = "list_comment2").text)
            up_count = int(item.find_all("td", class_ = "eng list_vspace")[2].text.split(" - ")[0])
            down_count = int(item.find_all("td", class_ = "eng list_vspace")[2].text.split(" - ")[1])
            if up_count >=5:
                if (Deal.objects.filter(link__iexact=link).count())==0:
                    Deal(image_url=image, title=title, link = link,
                        reply_count=reply_count, up_count=up_count).save()
                    bot.sendMessage(-1001840768438, '{} {}'.format(title, link))
        except Exception as e:
            #print(e)
            continue