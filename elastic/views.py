from django.http import JsonResponse
from django.shortcuts import render
from elasticsearch import Elasticsearch
from rest_framework.views import APIView
from rest_framework.response import Response
import json

es = Elasticsearch(
    cloud_id='buyornot:YXAtbm9ydGhlYXN0LTIuYXdzLmVsYXN0aWMtY2xvdWQuY29tOjkyNDMkZDcyODFhN2RiYTVhNDQ5MjhlOTEzMjBlMzllZjUxNTMkYmUzZjA1NjgyZDU5NGNmZmJkNTYxNjM5OWNlN2FiNTc=',
    basic_auth=('elastic', 'Orf5PC90BVmMMuVU5cKoTyrs'),
)

class MapDetail(APIView):
    def get(self, request, format=None):
        global es

        res = es.search(index='시군구위도경도')

        ans = []
        dic = {'positions':[]}
        for i in res['hits']['hits']:

            dic['positions'].append({'lat': i['_source']['y'], 'lng':i['_source']['x'], 'gu':i['_source']['SIG_KOR_NM']})
            # dic[i['_source']['SIG_KOR_NM']] = {'x': i['_source']['x'], 'y': i['_source']['y']}
            # ans.append(dic)

        # print(res['hits']['hits'])

        return Response(dic)

class FindByGu(APIView):
    def get(self, request, format=None):
        global es
        guName = request.GET['guName']
        res = es.search(index='시군구위도경도', query={
            'match': {
                'SIG_KOR_NM': guName
            }
        }, size=21)
        # print(res)

        guCode = res['hits']['hits'][0]['_source']['SIG_CD']

        res = es.search(index='상권영역', query={
            'match': {
                '시군구_코드': guCode
            }
        }, size=1000)
        # print(res['hits']['hits'])
        ans = []
        for i in res['hits']['hits']:
            ans.append(i['_source'])
        return Response(ans)

class Population(APIView):
    def get(self, request, format=None):
        global es
        ans = {}
        cCode = request.GET['cCode']
        res = es.search(index='상권-생활인구', query={
            "bool": {
                "must": [
                    {
                        "match": {
                            "상권_코드_명": cCode
                        }
                    },
                    {
                        "match": {
                            "기준 년코드": 2021
                        }
                    },
                    {
                        "match": {
                            "기준_분기_코드": 4
                        }
                    }
                ]
            }
        }, size=21)
        # print(res)
        ans['상권-생활인구'] = res['hits']['hits'][0]['_source']

        res = es.search(index='상권-상주인구', query={
            "bool": {
                "must": [
                    {
                        "match": {
                            "상권 코드 명": cCode
                        }
                    },
                    {
                        "match": {
                            "기준_년_코드": 2021
                        }
                    },
                    {
                        "match": {
                            "기준_분기_코드": 4
                        }
                    }
                ]
            }
        }, size=21)

        ans['상권-상주인구'] = res['hits']['hits'][0]['_source']

        res = es.search(index='상권-직장인구', query={
            "bool": {
                "must": [
                    {
                        "match": {
                            "상권_코드_명": cCode
                        }
                    },
                    {
                        "match": {
                            "기준_년월_코드": 2021
                        }
                    },
                    {
                        "match": {
                            "기준_분기_코드": 4
                        }
                    }
                ]
            }
        }, size=21)

        ans['상권-직장인구'] = res['hits']['hits'][0]['_source']

        res = es.search(index='상권배후지-생활인구', query={
            "bool": {
                "must": [
                    {
                        "match": {
                            "상권_코드_명": cCode
                        }
                    },
                    {
                        "match": {
                            "기준_년_코드": 2021
                        }
                    },
                    {
                        "match": {
                            "기준_분기_코드": 4
                        }
                    }
                ]
            }
        }, size=21)
        # print(res)
        ans['상권배후지-생활인구'] = res['hits']['hits'][0]['_source']

        res = es.search(index='상권배후지-상주인구', query={
            "bool": {
                "must": [
                    {
                        "match": {
                            "상권_코드_명": cCode
                        }
                    },
                    {
                        "match": {
                            "기준_년_코드": 2021
                        }
                    },
                    {
                        "match": {
                            "기준_분기_코드": 4
                        }
                    }
                ]
            }
        }, size=21)

        ans['상권배후지-상주인구'] = res['hits']['hits'][0]['_source']

        res = es.search(index='상권배후지-직장인구', query={
            "bool": {
                "must": [
                    {
                        "match": {
                            "상권_코드_명": cCode
                        }
                    },
                    {
                        "match": {
                            "기준_년_코드": 2021
                        }
                    },
                    {
                        "match": {
                            "기준_분기_코드": 4
                        }
                    }
                ]
            }
        }, size=21)

        ans['상권배후지-직장인구'] = res['hits']['hits'][0]['_source']

        return Response(ans)

class Sales(APIView):
    def get(self, request, format=None):
        global es
        cCode = request.GET['cCode']
        serviceCode = request.GET['serviceCode']
        res = es.search(index='상권-추정매출', query={
            "bool": {
                "must": [
                    {
                        "match": {
                            "상권_코드_명": cCode
                        }
                    },
                    {
                        "match": {
                            "서비스_업종_코드_명": serviceCode
                        }
                    }
                ]
            }
        })
        ans = []
        for i in res['hits']['hits']:
            ans.append(i['_source'])
        return Response(ans)

class Store(APIView):
    def get(self, request, format=None):
        global es
        cCode = request.GET['cCode']
        serviceCode = request.GET['serviceCode']
        res = es.search(index='상권-점포', query={
            "bool": {
                "must": [
                    {
                        "match": {
                            "상권_코드_명": cCode
                        }
                    },
                    {
                        "match": {
                            "서비스_업종_코드_명": serviceCode
                        }
                    }
                ]
            }
        })
        ans = []
        for i in res['hits']['hits']:
            ans.append(i['_source'])

        return Response(ans)

class StoreChange(APIView):
    def get(self, request, format=None):
        global es
        cCode = request.GET['cCode']
        res = es.search(index='상권-상권변화지표', query={
            "bool": {
                "must": [
                    {
                        "match": {
                            "상권_코드_명": cCode
                        }
                    }
                ]
            }
        })
        ans = []
        for i in res['hits']['hits']:
            ans.append(i['_source'])

        return Response(ans)


class Facilities(APIView):
    def get(self, request, format=None):
        global es
        cCode = request.GET['cCode']
        res = es.search(index='상권-상권변화지표', query={
            "bool": {
                "must": [
                    {
                        "match": {
                            "상권_코드_명": cCode
                        }
                    }
                ]
            }
        })
        ans = []
        for i in res['hits']['hits']:
            ans.append(i['_source'])

        return Response(ans)

def index(request):
    return render(request, 'elastic/index.html')

def polygon(request):
    f = open('C:\django_workspace\KimHwangBaeStreet\elastic\polygon.geojson', encoding='utf-8')
    f2 = open('C:\django_workspace\KimHwangBaeStreet\elastic\polygon2.geojson', encoding='utf-8')
    context = json.load(f),
    f.close()
    # print(context)
    return JsonResponse(context)