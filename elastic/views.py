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


from rest_framework.views import APIView
from rest_framework.response import Response

from . import models

class TestDetail(APIView):
    def get(self, request, format=None):
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

        return Response(res['hits']['hits'])

class MapDetail(APIView):
    def get(self, request, format=None):
        es = Elasticsearch(
            cloud_id='buyornot:YXAtbm9ydGhlYXN0LTIuYXdzLmVsYXN0aWMtY2xvdWQuY29tOjkyNDMkZDcyODFhN2RiYTVhNDQ5MjhlOTEzMjBlMzllZjUxNTMkYmUzZjA1NjgyZDU5NGNmZmJkNTYxNjM5OWNlN2FiNTc=',
            basic_auth=('elastic', 'Orf5PC90BVmMMuVU5cKoTyrs'),
        )

        res = es.search(index='시군구위도경도')

        ans = []
        for i in res['hits']['hits']:
            dic = {}

            dic[i['_source']['SIG_KOR_NM']] = {'x':i['_source']['x'], 'y':i['_source']['y']}
            ans.append(dic)

        # print(res['hits']['hits'])

        return Response(ans)

# searchAPI()

