from googlesearch import GoogleSearch
import CRUD
import time
import threading

input_txt_path_name = 'to_search.txt'
GS = GoogleSearch()

def show_contents():
    # show all contents

    contents = CRUD.read_content()
    for content in contents:
        print(content.title+': '+content.url)

def get_title_and_url_by_keyword(keyword, num_results):
    # like the name

    existing_keyword = CRUD.read_keyword(keyword)
    if len(existing_keyword) == 0:
        CRUD.create_keyword(keyword)
        existing_keyword.append(CRUD.read_keyword(keyword))
    else:
        CRUD.delete_content(existing_keyword[0].id)

    response = GS.search(keyword, num_results=num_results)
    for result in response.results:
        CRUD.create_content(result.title, result.url, existing_keyword[0])

def get_title_and_url(input_txt, num_results=20):
    # get related titles and urls from google

    # frist read keywords
    keywords = []
    with open(input_txt, 'r') as f:
        line = f.readline()                
        while line:
            keywords.append(line[:-1])
            line = f.readline()
            
    # then get the targets and put them into the database
    for keyword in keywords:
        get_title_and_url_by_keyword(keyword, num_results)

if __name__=='__main__':
    show_contents()

    while True:
        try:
            get_title_and_url(input_txt_path_name)
            print('database refreshed')
        except:
            print('a problem encountered')
        time.sleep(1)
