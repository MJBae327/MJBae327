from django.shortcuts import render, redirect
from .models import Keyword, Trend
from .forms import KeywordForm
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import matplotlib.pyplot as plt

# Create your views here.
def keyword(request):
    keywords = Keyword.objects.all()
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        if form.is_valid():
            keyword = form.save()
            return redirect('trends:keyword', keyword.pk)
    else:
        form = KeywordForm()
    context = {
        'keywords': keywords,
        'form': form,
    }
    return render(request, 'trends/keyword.html', context)


def keyword_detail(request, pk):
    keyword = Keyword.objects.get(pk=pk)
    keyword.delete()
    return redirect('trends:keyword')

def get_google_data(keyword):
    url = f'https://www.google.com/search?q={keyword}'
    driver = webdriver.Chrome()
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    result = soup.select_one('#result-stats')
    result = result.get_text()
    num = ''
    for i in range(len(result)):
        if result[i] == '개':
            break
        if result[i].isdigit():
            num += result[i]
    return int(num)


def crawling(request):
    keywords = Keyword.objects.all()

    for keyword in keywords:
        try:
            name = keyword.name
            trend = Trend.objects.get(name=name)
            result = get_google_data(keyword.name)
            trend.result = result
            trend.save()
        except:
            name = keyword.name
            result = get_google_data(keyword.name)
            Trend.objects.create(name=name, result=result)
            trend.save()
    
    trends= Trend.objects.all()
    context = {
        'trends' : trends,
    }
    return render(request, 'trends/crawling.html', context)

def crawling_histogram(request):
    pass


def crawling_advanced(request):
    pass