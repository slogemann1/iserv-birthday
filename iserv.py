from datetime import date, timedelta
import requests
import random
import csv
import re
from PIL import Image
import random
import colorsys
from io import BytesIO

# Read files
logins_csv = open("logins.txt")
logins = csv.reader(logins_csv, delimiter=",")

birthday_file = open("birthday_payload.txt")
birthday_payload = birthday_file.read()

hue_file = open("hue.txt")
hue = int(hue_file.read())

def main():
    for row in logins:
        if len(row) < 2:
            continue
        else:
            change_birthday(row[0], row[1])
    change_hue()
    return


def change_birthday(username, password):
    # Setup Session
    session = requests.Session()

    # Get Login Cookies
    login_url = "https://fkggoettingen.de/iserv/app/login?target=%2Fiserv%2F"
    login_data = "_username=" + username + "&_password=" + password
    login_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Content-Length": str(len(login_url)),
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://fkggoettingen.de",
        "Referrer": "https://fkggoettingen.de/iserv/app/login?target=%2Fiserv%2F",
        "Upgrade-Insecure-Requests": "1",
        "Connection": "keep-alive"
    }
    session.post(url=login_url, data=login_data, headers=login_headers)

    # Send Get Request to Retrive Form Token
    form_url = "https://fkggoettingen.de/iserv/profile/public/edit"
    form_response = session.get(url=form_url)

    # Get the Form Token from the Data
    token_regex = "id=\"publiccontact__token\"[\\w\\W]*?value=\"([^\"]*)\""
    token_match = re.search(token_regex, form_response.text)
    token = ""
    if token_match == None:
        print("Error regex failed to find token")
        exit()
    else:
        token = token_match.group(1)

    # Make Date String
    years = random.randint(17, 20)
    days = 6
    today = date.today()
    today_birth = date(day = today.day, month = today.month, year = today.year - years)
    birthday_date = today_birth + timedelta(days = days)
    
    birthday = birthday_date.strftime("%d.%m.%Y")

    # Send Post Request to Change
    change_url = "https://fkggoettingen.de/iserv/profile/public/edit"
    change_data = create_payload(token, birthday)
    change_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
        "Content-Length": str(len(birthday_payload)),
        "Content-Type": "application/x-www-form-urlencoded"
    }

    change_response = session.post(url=change_url, data=change_data, headers=change_headers)
    
    return

def create_payload(token, birthday):
    # Get Color for Image
    # hue_input = hue / 256.0
    # color = colorsys.hsv_to_rgb(hue_input, 1.0, 0.75)
    # color = (int(color[0] * 256), int(color[1] * 256), int(color[2] * 256))

    # Create Image
    # img = Image.new("RGB", (256, 256), color)
    # buffer = BytesIO()
    # img.save(buffer, format="png")
    # image_data = bytes(buffer.getbuffer())

    # Create Payload
    payload = birthday_payload.replace("YOUR_BIRTHDAY_HERE", birthday).replace("YOUR_TOKEN_HERE", token)
    # payload = payload.split("YOUR_IMAGE_HERE")
    # payload_1 = payload[0]
    # payload_2 = payload[1]
    # payload = bytearray(payload_1, "utf-8")
    # payload.extend(image_data)
    # payload.extend(bytes(payload_2, "utf-8"))

    return payload

def change_hue():
    new_hue = hue + 10 % 255
    hue_file = open("hue.txt", "w+")
    hue_file.write(str(new_hue))

if __name__ == "__main__":
    main()
