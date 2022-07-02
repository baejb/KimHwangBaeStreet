from django.shortcuts import render
from elasticsearch import Elasticsearch

def searchAPI():
    es = Elasticsearch(
        cloud_id='buyornot:YXAtbm9ydGhlYXN0LTIuYXdzLmVsYXN0aWMtY2xvdWQuY29tOjkyNDMkZDcyODFhN2RiYTVhNDQ5MjhlOTEzMjBlMzllZjUxNTMkYmUzZjA1NjgyZDU5NGNmZmJkNTYxNjM5OWNlN2FiNTc=',
        basic_auth=('elastic', 'Orf5PC90BVmMMuVU5cKoTyrs'),
    )

    res = es.search(index=['상권영역', '상권-생활인구'], query={
        'match': {
            '상권_코드_명': '신촌역 6번'
        }
    }, size=21)
    print(res['hits']['hits'])


searchAPI()

