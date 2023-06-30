import json

f = open('mock.json', encoding='utf-8')

data = json.load(f)

# def search_title(title):
#     for keyval in data:
#         if title.lower() == keyval['title'].lower():
#             return keyval['title']
        
# search_title('Эликсир любви')

# for key in data:
#     print(data[key])

# print(data['title'])

# def find_book(title):
#     for lines in data:


print(data['variants'][0]['price'])
