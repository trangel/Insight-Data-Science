import urllib.request

text_request="https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=autism&prop=revisions&rvprop=content&format=json"

articles=urllib.request.urlopen(text_request).read()

print(articles)
