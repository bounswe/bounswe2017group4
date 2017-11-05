import urllib.request
import json
class bookObj:
    def __init__(self, id, title, authors, publisher, description, pageCount, categories):
        self.id = id
        self.title = title
        self.authors = authors
        self.publisher = publisher
        self.description = description
        self.pageCount = pageCount
        self.categories = categories
bookList = []
url = 'https://www.googleapis.com/books/v1/volumes?q='
search_text = input('Enter a search query: ')
search_text = search_text.replace(' ', '+')
#language = input('Enter a language code: ')
#maxResults = input('Enter how many results do you want to see: ')
full_url = url + search_text + '&maxResults=' + '40'
print(full_url)
response = urllib.request.urlopen(full_url).read()
json_obj = str(response, 'utf-8')
data = json.loads(json_obj)

print('---------------------------')

for item in data['items']:
    volumeInfo = item['volumeInfo']
    id = ''
    title = ''
    authors = []
    publisher = ''
    description = ''
    pageCount = ''
    categories = []
    if 'id' in item:
        id = item['id']
    if 'title' in volumeInfo:
        print('Name: '+item['volumeInfo']['title'])
        title = item['volumeInfo']['title']
    if 'authors' in volumeInfo:
        print('Author(s): ', end='')
        for author in item['volumeInfo']['authors']:
            print(author+'\t', end='')
            authors.append(author)
        print()
    if 'categories' in volumeInfo:
        print('Category(s): ', end='')
        for category in item['volumeInfo']['categories']:
            print(category+'\t', end='')
            categories.append(category)
        print()
    if 'pageCount' in volumeInfo:
        print('Page Count: ' + str(item['volumeInfo']['pageCount']))
        pageCount = str(item['volumeInfo']['pageCount'])
    if 'description' in volumeInfo:
        description = item['volumeInfo']['description']
    if 'publisher' in volumeInfo:
        publisher = item['volumeInfo']['publisher']
    bookElem = bookObj(id,title,authors,publisher,description,pageCount,categories)
    bookList.append(bookElem)
    print('---------------------------')
i = 1
for bookElem in bookList:
    #print(str(i)+'. '+", ".join(bookElem.authors))
    if bookElem.pageCount!='':
        if(int(bookElem.pageCount)<200):
            print(str(i)+'. '+bookElem.title + ',\t '+bookElem.pageCount)
        i+=1
