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


class GraphTest(APIView):
    def get(self, request, format=None):
        global es

        result = {
            "점포수": {
                "label": ['2021년 1분기', '2021년 2분기', '2021년 3분기', '2021년 4분기'],
                "data": []
            },
            "일반/프랜차이즈": {
                "label": ["일반점포", "프랜차이즈"],
                "data": [0, 0]
            },
            "개업수": {
                "label": ['2021년 1분기', '2021년 2분기', '2021년 3분기', '2021년 4분기'],
                "data": []
            },
            "폐업수": {
                "label": ['2021년 1분기', '2021년 2분기', '2021년 3분기', '2021년 4분기'],
                "data": []
            }
        }

        cCode = request.GET['cCode']
        serviceCode = request.GET['serviceCode']

        for num in [1, 2, 3, 4]:

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
                        },
                        {
                            "match": {
                                "기준_분기_코드": num
                            }
                        },
                        {
                            "match": {
                                "기준_년_코드": 2021
                            }
                        }
                    ]
                }
            }, size=1000)

            result["점포수"]["data"].append(res['hits']['hits'][0]['_source']['점포_수'])

            if num == 4:
                result["일반/프랜차이즈"]["data"][0] = res['hits']['hits'][0]['_source']['점포_수'] - res['hits']['hits'][0]['_source']['프랜차이즈_점포_수']
                result["일반/프랜차이즈"]["data"][1] = res['hits']['hits'][0]['_source']['프랜차이즈_점포_수']

            result["개업수"]["data"].append(res['hits']['hits'][0]['_source']['개업_점포_수'])
            result["폐업수"]["data"].append(res['hits']['hits'][0]['_source']['폐업_점포_수'])

        return Response(result)


class MapDetail(APIView):
    def get(self, request, format=None):
        global es

        res = es.search(index='시군구위도경도', size=1000)

        ans = []
        dic = {'positions': []}
        for i in res['hits']['hits']:
            cnt = es.search(index='상권영역', query={
                "match": {
                    "시군구_코드": i['_source']['SIG_CD']
                }
            }, track_total_hits=True)
            dic['positions'].append(
                {'lat': i['_source']['y'], 'lng': i['_source']['x'], 'gu': i['_source']['SIG_KOR_NM'],
                 'cnt': cnt['hits']['total']['value']})
            # dic[i['_source']['SIG_KOR_NM']] = {'x': i['_source']['x'], 'y': i['_source']['y']}
            # ans.append(dic)

        # print(res['hits']['hits'])

        return Response(dic)


class FindByGu_key(APIView):
    def get(self, request, format=None):
        global es
        guName = request.GET['guName']
        res = es.search(index='시군구위도경도', query={
            'prefix': {
                'SIG_KOR_NM': guName
            }
        }, size=21)
        # print(res)
        dic = {'searchList': []}

        for g in res['hits']['hits']:
            dic['searchList'].append(g['_source']['SIG_KOR_NM'])

        print(dic)
        # i = res['hits']['hits'][0]
        #
        # dic['positions'] = {'lat': i['_source']['y'], 'lng': i['_source']['x'], 'gu': i['_source']['SIG_KOR_NM']}

        return Response(dic)

class FindByGu_enter(APIView):
    def get(self, request, format=None):
        global es
        guName = request.GET['guName']
        res = es.search(index='시군구위도경도', query={
            'fuzzy': {
                'SIG_KOR_NM': guName
            }
        }, size=21)
        # print(res)

        if not res['hits']['hits']:
            res = es.search(index='시군구위도경도', query={
                'prefix': {
                    'SIG_KOR_NM': guName
                }
            }, size=21)

        if not res['hits']['hits']:
            return Response(False)

        dic = {'positions': {}}
        i = res['hits']['hits'][0]

        dic['positions'] = {'lat': i['_source']['y'], 'lng': i['_source']['x'], 'gu': i['_source']['SIG_KOR_NM']}

        return Response(dic)

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
        }, size=1000)
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
        }, size=1000)

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
        }, size=1000)

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
        }, size=1000)
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
        }, size=1000)

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
        }, size=1000)

        ans['상권배후지-직장인구'] = res['hits']['hits'][0]['_source']

        return Response(ans)


class Sales(APIView):
    def get(self, request, format=None):
        global es
        cCode = request.GET['cCode']
        serviceCode = request.GET['serviceCode']
        if serviceCode == 'all':
            allList = ['분식전문점', '한식음식점', '일식음식점', '치킨전문점', '중식음식점', '양식음식점', '제과점', '패스트푸드점', '호프-간이주점', '커피-음료']
            res = es.search(index='상권-추정매출', query={
                "bool": {
                    "must": [
                        {
                            "match": {
                                "상권_코드_명": cCode
                            }
                        },
                        {
                            "terms": {
                                "서비스_업종_코드_명": allList
                            }
                        }
                    ]
                }
            }, size=1000)
        else:
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
            }, size=1000)
        ans = []
        for i in res['hits']['hits']:
            ans.append(i['_source'])
        return Response(ans)


class Store(APIView):
    def get(self, request, format=None):
        global es
        cCode = request.GET['cCode']
        serviceCode = request.GET['serviceCode']
        if serviceCode == 'all':
            allList = ['분식전문점', '한식음식점', '일식음식점', '치킨전문점', '중식음식점', '양식음식점', '제과점', '패스트푸드점', '호프-간이주점', '커피-음료']
            res = es.search(index='상권-점포', query={
                "bool": {
                    "must": [
                        {
                            "match": {
                                "상권_코드_명": cCode
                            }
                        },
                        {
                            "terms": {
                                "서비스_업종_코드_명": allList
                            }
                        }
                    ]
                }
            }, size=1000)
        else:
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
            }, size=1000)
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
        }, size=1000)
        ans = []
        for i in res['hits']['hits']:
            ans.append(i['_source'])

        return Response(ans)


class Facilities(APIView):
    def get(self, request, format=None):
        global es
        cCode = request.GET['cCode']
        res = es.search(index='상권-집객시설', query={
            "bool": {
                "must": [
                    {
                        "match": {
                            "상권_코드_명": cCode
                        }
                    }
                ]
            }
        }, size=1000)
        ans = []
        for i in res['hits']['hits']:
            ans.append(i['_source'])

        return Response(ans)


def index(request):
    return render(request, 'elastic/index.html')

def main(request):
    return render(request, 'elastic/main.html')

def polygon(request):
    f = open('elastic\polygon.geojson', encoding='utf-8')
    context = json.load(f)
    f.close()
    # print(context)
    return JsonResponse(context)


def polygon2(request):
    f = open('elastic\polygon2.geojson', encoding='utf-8')
    context = json.load(f)
    f.close()
    # print(context)
    return JsonResponse(context)

