# from django.shortcuts import render
#
# # Create your views here.
# from elasticsearch_dsl import Q
# from booking_system.documents import CountryDocument
#
#
# # Выполняет поиск всех статей, в названии которых есть «How to».
# query = 'Kyrgyzstan'
# q = Q(
#      'multi_match',
#      query=query,
#      fields=[
#          'country_name'
#      ])
# search = CountryDocument.search().query(q)
# response = search.execute()
#
# # распечатать все хиты
# for hit in search:
#     print(hit.title)


import itertools
print(list(itertools.permutations([1,2,3])))