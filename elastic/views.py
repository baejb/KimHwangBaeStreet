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

class GraphJSON(APIView):
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
            },
            "매출-요일별": {
                "label": ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일'],
                "data": [0, 0, 0, 0, 0, 0, 0]
            },
            "매출-시간대별": {
                "label": ['00~06', '06~11', '11~14', '14~17', '17~21', '21~24'],
                "data": [0, 0, 0, 0, 0, 0]
            },
            "매출-성별": {
                "label": ['남성', '여성'],
                "data": [0, 0]
            },
            "매출-연령대별": {
                "label": ['10대', '20대', '30대', '40대', '50대', '60대 이상'],
                "data": [0, 0, 0, 0, 0, 0]
            },
            "유동-총": 0,
            "유동-성별": {
                "label": ['남성', '여성'],
                "data": [0, 0]
            },
            "유동-연령대별": {
                "label": ['10대', '20대', '30대', '40대', '50대', '60대 이상'],
                "data": [0, 0, 0, 0, 0, 0]
            },
            "유동-요일별": {
                "label": ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일'],
                "data": [0, 0, 0, 0, 0, 0, 0]
            },
            "유동-시간대별": {
                "label": ['00~06', '06~11', '11~14', '14~17', '17~21', '21~24'],
                "data": [0, 0, 0, 0, 0, 0]
            },
            "주거-총": 0,
            "주거-연령대별": {
                "label": ['10대', '20대', '30대', '40대', '50대', '60대 이상'],
                "data": [0, 0, 0, 0, 0, 0]
            },
            "직장-총": 0,
            "직장-연령대별": {
                "label": ['10대', '20대', '30대', '40대', '50대', '60대 이상'],
                "data": [0, 0, 0, 0, 0, 0]
            },
            "집객시설수" : 0
        }

        cCode = request.GET['cCode']
        serviceCode = request.GET['serviceCode']

        # 점포
        for num in [1, 2, 3, 4]:

            res1 = es.search(index='상권-점포', query={
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

            if res1['hits']['hits'] :

                result["점포수"]["data"].append(res1['hits']['hits'][0]['_source']['점포_수'])

                if num == 4:
                    result["일반/프랜차이즈"]["data"][0] = res1['hits']['hits'][0]['_source']['점포_수'] - \
                                                    res1['hits']['hits'][0]['_source']['프랜차이즈_점포_수']
                    result["일반/프랜차이즈"]["data"][1] = res1['hits']['hits'][0]['_source']['프랜차이즈_점포_수']

                result["개업수"]["data"].append(res1['hits']['hits'][0]['_source']['개업_점포_수'])
                result["폐업수"]["data"].append(res1['hits']['hits'][0]['_source']['폐업_점포_수'])
            else:
                result["점포수"]["data"].append(0)
                result["개업수"]["data"].append(0)
                result["폐업수"]["data"].append(0)

        # 추정매출
        res2 = es.search(index='상권-추정매출', query={
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
                            "기준_분기_코드": 4
                        }
                    }
                ]
            }
        }, size=1000)

        if res2['hits']['hits']:

            result["매출-요일별"]["data"] = [res2['hits']['hits'][0]['_source']['월요일_매출_금액'],
                                        res2['hits']['hits'][0]['_source']['화요일_매출_금액'],
                                        res2['hits']['hits'][0]['_source']['수요일_매출_금액'],
                                        res2['hits']['hits'][0]['_source']['목요일_매출_금액'],
                                        res2['hits']['hits'][0]['_source']['금요일_매출_금액'],
                                        res2['hits']['hits'][0]['_source']['토요일_매출_금액'],
                                        res2['hits']['hits'][0]['_source']['일요일_매출_금액']]

            result["매출-시간대별"]["data"] = [res2['hits']['hits'][0]['_source']['시간대_00~06_매출_금액'],
                                         res2['hits']['hits'][0]['_source']['시간대_06~11_매출_금액'],
                                         res2['hits']['hits'][0]['_source']['시간대_11~14_매출_금액'],
                                         res2['hits']['hits'][0]['_source']['시간대_14~17_매출_금액'],
                                         res2['hits']['hits'][0]['_source']['시간대_17~21_매출_금액'],
                                         res2['hits']['hits'][0]['_source']['시간대_21~24_매출_금액']]

            result["매출-연령대별"]["data"] = [res2['hits']['hits'][0]['_source']['연령대_10_매출_금액'],
                                        res2['hits']['hits'][0]['_source']['연령대_20_매출_금액'],
                                        res2['hits']['hits'][0]['_source']['연령대_30_매출_금액'],
                                        res2['hits']['hits'][0]['_source']['연령대_40_매출_금액'],
                                        res2['hits']['hits'][0]['_source']['연령대_50_매출_금액'],
                                        res2['hits']['hits'][0]['_source']['연령대_60_이상_매출_금액']]

            result["매출-성별"]["data"] = [res2['hits']['hits'][0]['_source']['남성_매출_금액'],
                                       res2['hits']['hits'][0]['_source']['여성_매출_금액']]

        # 인구
        res3 = es.search(index='상권-생활인구', query={
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

        if res3['hits']['hits']:
            result["유동-총"] = res3['hits']['hits'][0]['_source']['총_생활인구_수']

            result["유동-성별"]["data"] = [res3['hits']['hits'][0]['_source']['남성_생활인구_수'],
                                       res3['hits']['hits'][0]['_source']['여성_생활인구_수']]

            result["유동-연령대별"]["data"] = [res3['hits']['hits'][0]['_source']['연령대_10_생활인구_수'],
                                        res3['hits']['hits'][0]['_source']['연령대_20_생활인구_수'],
                                        res3['hits']['hits'][0]['_source']['연령대_30_생활인구_수'],
                                        res3['hits']['hits'][0]['_source']['연령대_40_생활인구_수'],
                                        res3['hits']['hits'][0]['_source']['연령대_50_생활인구_수'],
                                        res3['hits']['hits'][0]['_source']['연령대_60_이상_생활인구_수']]

            result["유동-요일별"]["data"] = [res3['hits']['hits'][0]['_source']['월요일_생활인구_수'],
                                        res3['hits']['hits'][0]['_source']['화요일_생활인구_수'],
                                        res3['hits']['hits'][0]['_source']['수요일_생활인구_수'],
                                        res3['hits']['hits'][0]['_source']['목요일_생활인구_수'],
                                        res3['hits']['hits'][0]['_source']['금요일_생활인구_수'],
                                        res3['hits']['hits'][0]['_source']['토요일_생활인구_수'],
                                        res3['hits']['hits'][0]['_source']['일요일_생활인구_수']]

            result["유동-시간대별"]["data"] = [res3['hits']['hits'][0]['_source']['시간대_1_생활인구_수'],
                                         res3['hits']['hits'][0]['_source']['시간대_2_생활인구_수'],
                                         res3['hits']['hits'][0]['_source']['시간대_3_생활인구_수'],
                                         res3['hits']['hits'][0]['_source']['시간대_4_생활인구_수'],
                                         res3['hits']['hits'][0]['_source']['시간대_5_생활인구_수'],
                                         res3['hits']['hits'][0]['_source']['시간대_6_생활인구_수']]

        res3 = es.search(index='상권-직장인구', query={
            "bool": {
                "must": [
                    {
                        "match": {
                            "상권_코드_명": cCode
                        }
                    },
                    {
                        "match": {
                            "기준_분기_코드": 4
                        }
                    },
                    {
                        "match": {
                            "기준_년월_코드": 2021
                        }
                    }
                ]
            }
        }, size=1000)

        if res3['hits']['hits']:
            result["직장-총"] = res3['hits']['hits'][0]['_source']['총_직장_인구_수']

            result["직장-연령대별"]['data'] = [res3['hits']['hits'][0]['_source']['연령대_10_직장_인구_수'],
                                        res3['hits']['hits'][0]['_source']['연령대_20_직장_인구_수'],
                                        res3['hits']['hits'][0]['_source']['연령대_30_직장_인구_수'],
                                        res3['hits']['hits'][0]['_source']['연령대_40_직장_인구_수'],
                                        res3['hits']['hits'][0]['_source']['연령대_50_직장_인구_수'],
                                        res3['hits']['hits'][0]['_source']['연령대_60_이상_직장_인구_수']]

        res3 = es.search(index='상권-상주인구', query={
            "bool": {
                "must": [
                    {
                        "match": {
                            "상권 코드 명": cCode
                        }
                    },
                    {
                        "match": {
                            "기준_분기_코드": 4
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

        if res3['hits']['hits']:
            result["주거-총"] = res3['hits']['hits'][0]['_source']['총 상주인구 수']

            result["주거-연령대별"]['data'] = [res3['hits']['hits'][0]['_source']['연령대 10 상주인구 수'],
                                        res3['hits']['hits'][0]['_source']['연령대 20 상주인구 수'],
                                        res3['hits']['hits'][0]['_source']['연령대 30 상주인구 수'],
                                        res3['hits']['hits'][0]['_source']['연령대 40 상주인구 수'],
                                        res3['hits']['hits'][0]['_source']['연령대 50 상주인구 수'],
                                        res3['hits']['hits'][0]['_source']['연령대 60 이상 상주인구 수']]

        # 집객시설
        res4 = es.search(index='상권-집객시설', query={
            "bool": {
                "must": [
                    {
                        "match": {
                            "상권_코드_명": cCode
                        }
                    },
                    {
                        "match": {
                            "기준_분기_코드": 4
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

        if res4['hits']['hits']:
            result["집객시설수"] = res4['hits']['hits'][0]['_source']['집객시설_수']

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


# class Population(APIView):
#     def get(self, request, format=None):
#         global es
#         ans = {}
#         cCode = request.GET['cCode']
#         res = es.search(index='상권-생활인구', query={
#             "bool": {
#                 "must": [
#                     {
#                         "match": {
#                             "상권_코드_명": cCode
#                         }
#                     },
#                     {
#                         "match": {
#                             "기준 년코드": 2021
#                         }
#                     },
#                     {
#                         "match": {
#                             "기준_분기_코드": 4
#                         }
#                     }
#                 ]
#             }
#         }, size=1000)
#         # print(res)
#         ans['상권-생활인구'] = res['hits']['hits'][0]['_source']
#
#         res = es.search(index='상권-상주인구', query={
#             "bool": {
#                 "must": [
#                     {
#                         "match": {
#                             "상권 코드 명": cCode
#                         }
#                     },
#                     {
#                         "match": {
#                             "기준_년_코드": 2021
#                         }
#                     },
#                     {
#                         "match": {
#                             "기준_분기_코드": 4
#                         }
#                     }
#                 ]
#             }
#         }, size=1000)
#
#         ans['상권-상주인구'] = res['hits']['hits'][0]['_source']
#
#         res = es.search(index='상권-직장인구', query={
#             "bool": {
#                 "must": [
#                     {
#                         "match": {
#                             "상권_코드_명": cCode
#                         }
#                     },
#                     {
#                         "match": {
#                             "기준_년월_코드": 2021
#                         }
#                     },
#                     {
#                         "match": {
#                             "기준_분기_코드": 4
#                         }
#                     }
#                 ]
#             }
#         }, size=1000)
#
#         ans['상권-직장인구'] = res['hits']['hits'][0]['_source']
#
#         res = es.search(index='상권배후지-생활인구', query={
#             "bool": {
#                 "must": [
#                     {
#                         "match": {
#                             "상권_코드_명": cCode
#                         }
#                     },
#                     {
#                         "match": {
#                             "기준_년_코드": 2021
#                         }
#                     },
#                     {
#                         "match": {
#                             "기준_분기_코드": 4
#                         }
#                     }
#                 ]
#             }
#         }, size=1000)
#         # print(res)
#         ans['상권배후지-생활인구'] = res['hits']['hits'][0]['_source']
#
#         res = es.search(index='상권배후지-상주인구', query={
#             "bool": {
#                 "must": [
#                     {
#                         "match": {
#                             "상권_코드_명": cCode
#                         }
#                     },
#                     {
#                         "match": {
#                             "기준_년_코드": 2021
#                         }
#                     },
#                     {
#                         "match": {
#                             "기준_분기_코드": 4
#                         }
#                     }
#                 ]
#             }
#         }, size=1000)
#
#         ans['상권배후지-상주인구'] = res['hits']['hits'][0]['_source']
#
#         res = es.search(index='상권배후지-직장인구', query={
#             "bool": {
#                 "must": [
#                     {
#                         "match": {
#                             "상권_코드_명": cCode
#                         }
#                     },
#                     {
#                         "match": {
#                             "기준_년_코드": 2021
#                         }
#                     },
#                     {
#                         "match": {
#                             "기준_분기_코드": 4
#                         }
#                     }
#                 ]
#             }
#         }, size=1000)
#
#         ans['상권배후지-직장인구'] = res['hits']['hits'][0]['_source']
#
#         return Response(ans)
#
#
# class Sales(APIView):
#     def get(self, request, format=None):
#         global es
#         cCode = request.GET['cCode']
#         serviceCode = request.GET['serviceCode']
#         if serviceCode == 'all':
#             allList = ['분식전문점', '한식음식점', '일식음식점', '치킨전문점', '중식음식점', '양식음식점', '제과점', '패스트푸드점', '호프-간이주점', '커피-음료']
#             res = es.search(index='상권-추정매출', query={
#                 "bool": {
#                     "must": [
#                         {
#                             "match": {
#                                 "상권_코드_명": cCode
#                             }
#                         },
#                         {
#                             "terms": {
#                                 "서비스_업종_코드_명": allList
#                             }
#                         }
#                     ]
#                 }
#             }, size=1000)
#         else:
#             res = es.search(index='상권-추정매출', query={
#                 "bool": {
#                     "must": [
#                         {
#                             "match": {
#                                 "상권_코드_명": cCode
#                             }
#                         },
#                         {
#                             "match": {
#                                 "서비스_업종_코드_명": serviceCode
#                             }
#                         }
#                     ]
#                 }
#             }, size=1000)
#         ans = []
#         for i in res['hits']['hits']:
#             ans.append(i['_source'])
#         return Response(ans)
#
#
# class Store(APIView):
#     def get(self, request, format=None):
#         global es
#         cCode = request.GET['cCode']
#         serviceCode = request.GET['serviceCode']
#         if serviceCode == 'all':
#             allList = ['분식전문점', '한식음식점', '일식음식점', '치킨전문점', '중식음식점', '양식음식점', '제과점', '패스트푸드점', '호프-간이주점', '커피-음료']
#             res = es.search(index='상권-점포', query={
#                 "bool": {
#                     "must": [
#                         {
#                             "match": {
#                                 "상권_코드_명": cCode
#                             }
#                         },
#                         {
#                             "terms": {
#                                 "서비스_업종_코드_명": allList
#                             }
#                         }
#                     ]
#                 }
#             }, size=1000)
#         else:
#             res = es.search(index='상권-점포', query={
#                 "bool": {
#                     "must": [
#                         {
#                             "match": {
#                                 "상권_코드_명": cCode
#                             }
#                         },
#                         {
#                             "match": {
#                                 "서비스_업종_코드_명": serviceCode
#                             }
#                         }
#                     ]
#                 }
#             }, size=1000)
#         ans = []
#         for i in res['hits']['hits']:
#             ans.append(i['_source'])
#
#         return Response(ans)
#
#
# class StoreChange(APIView):
#     def get(self, request, format=None):
#         global es
#         cCode = request.GET['cCode']
#         res = es.search(index='상권-상권변화지표', query={
#             "bool": {
#                 "must": [
#                     {
#                         "match": {
#                             "상권_코드_명": cCode
#                         }
#                     }
#                 ]
#             }
#         }, size=1000)
#         ans = []
#         for i in res['hits']['hits']:
#             ans.append(i['_source'])
#
#         return Response(ans)
#
#
# class Facilities(APIView):
#     def get(self, request, format=None):
#         global es
#         cCode = request.GET['cCode']
#         res = es.search(index='상권-집객시설', query={
#             "bool": {
#                 "must": [
#                     {
#                         "match": {
#                             "상권_코드_명": cCode
#                         }
#                     }
#                 ]
#             }
#         }, size=1000)
#         ans = []
#         for i in res['hits']['hits']:
#             ans.append(i['_source'])
#
#         return Response(ans)


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
