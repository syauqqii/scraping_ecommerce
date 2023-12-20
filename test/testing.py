import http.client

url = "shopee.co.id"
path = "/api/v4/search/search_items?by=sales&keyword=tas&limit=60&newest=0&order=desc&page_type=search&scenario=PAGE_SEO_SEARCH&version=2"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin"
}

conn = http.client.HTTPSConnection(url)
conn.request("GET", path, headers=headers)
response = conn.getresponse()
print(response.read())

