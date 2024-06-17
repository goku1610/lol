import requests

# Read the file and extract the search terms
with open("list.txt", "r") as f:
    file_content = f.read()

final_file_list = []
for i in range(1, len(file_content.split('"')), 2):
    final_file_list.append(file_content.split('"')[i])

# Function to perform a Bing search
def bing_search(query, subscription_key):
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": query, "textDecorations": True, "textFormat": "HTML"}

    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    if "webPages" in search_results and "value" in search_results["webPages"]:
        first_link = search_results["webPages"]["value"][0]["url"]
        return first_link
    else:
        return None

subscription_key = "e635fcdf348e4a868154deb206dc0740"

all_pdf_links = []

for search_term in final_file_list:
    query = f"filetype:pdf  fund factsheet  {search_term}"
    first_link = bing_search(query, subscription_key)
    if first_link:
        all_pdf_links.append(first_link)
        print("link found: ", first_link)
    else:
        print(f"No link found for {search_term}")

print("All found PDF links:", all_pdf_links)

for i, link in enumerate(all_pdf_links, 1):
    print(f"Downloading file: {i}")

    try:
        response = requests.get(link)
        response.raise_for_status()

        with open(f"pdf{i+1}.pdf", 'wb') as pdf:
            pdf.write(response.content)

        print(f"File {i} downloaded successfully")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download file {i} from {link}: {e}")

print("All PDF files downloaded")