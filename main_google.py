import requests
import datetime
import time

x = 12
now = time.localtime()
list = [time.localtime(time.mktime((now.tm_year, now.tm_mon - n, 1, 0, 0, 0, 0, 0, 0)))[:2] for n in range(x)]

with open("list.txt", "r") as f:
    file = f.read()

final_file_list = []
for i in range(1, len(file.split('"')), 2):
    final_file_list.append(file.split('"')[i])

def google_search(query, api_key, cx):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {"q": query, "key": api_key, "cx": cx, "fileType": "pdf"}

    response = requests.get(search_url, params=params)
    response.raise_for_status()
    search_results = response.json()

    if "items" in search_results:
        first_link = search_results["items"][0]["link"]
        return first_link
    else:
        return None

api_key = "AIzaSyAPXrvCb07PgJ1aorQZ5dnRzgVI2yA4eP0"
cx = "b69351eef312142db"

all_pdf_links = []

for i in range(len(final_file_list)):
    for j in range(12):
        query = f" filetype:pdf fund factsheet {final_file_list[i] } after: {list[j][0]}-{list[j][1]}-1 before: {list[j][0]}-{list[j][1]}-31"
        first_link = google_search(query, api_key, cx)
        all_pdf_links.append(first_link)
        # with open("links_pdf3.txt", "a") as l:
        #     l.write(first_link + "\n")
        print(first_link)
# for i, link in enumerate(all_pdf_links, 1):
#     print(f"Downloading file: {i}")
#
#     try:
#         response = requests.get(link)
#         response.raise_for_status()
#
#         with open(f"pdf{i}.pdf", 'wb') as pdf:
#             pdf.write(response.content)
#
#         print(f"File {i} downloaded successfully")
#
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to download file {i} from {link}: {e}")
#
# print("All PDF files downloaded")
