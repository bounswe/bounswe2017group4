import urllib.request
import json

url = 'https://www.googleapis.com/books/v1/volumes?q='
search_text = input('Enter a search query: ')
search_text = search_text.replace(' ', '+')
language = input('Enter a language code: ')
maxResults = input('Enter how many results do you want to see: ')
full_url = url + search_text + '&langRestrict=' + language + '&maxResults=' + maxResults
response = urllib.request.urlopen(full_url).read()
json_obj = str(response, 'utf-8')
data = json.loads(json_obj)
print('---------------------------')
for item in data['items']:
    print('Name: '+item['volumeInfo']['title'])
    print('Author(s): ', end='')
    for author in item['volumeInfo']['authors']:
        print(author+'\t', end='')
    print()
    print('Category(s): ', end='')
    for category in item['volumeInfo']['categories']:
        print(category+'\t', end='')
    print()
    print('Page Count: ' + str(item['volumeInfo']['pageCount']))
    print('---------------------------')