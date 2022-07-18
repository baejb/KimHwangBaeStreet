from django.urls import path, include
from . import views

urlpatterns = [
    path('map/', views.MapDetail.as_view()), # 시군구위도경도
    path('gu/', views.FindByGu.as_view()), # 시군구명으로 상권영역
    path('population/',  views.Population.as_view()), # 인구
    path('sales/', views.Sales.as_view()), # 추정매출
    path('store/', views.Store.as_view()), # 점포
    path('store/change/', views.StoreChange.as_view()), # 상권변화지표
    path('facilities/', views.Facilities.as_view()), # 집객시설
]