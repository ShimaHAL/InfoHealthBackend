from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import requests
from bs4 import BeautifulSoup


def api_test(request):

    context = {
        "message": "Welcome to the InfoHealth API!"
    }


    return JsonResponse(context)

@require_POST
@csrf_exempt
def post_url(request):
    context={"message": "POST request received", "data": request.POST["url"]}
    return JsonResponse(context)

@require_POST
@csrf_exempt
def comment_url(request):

    url = request.POST["url"]
    res = requests.get(url)

    soup=BeautifulSoup(res.text, "html.parser")
    div = soup.find("div", {"class": "news-comment-plugin"})
    full_page_url = div["data-full-page-url"]
    topic_id = div["data-topic-id"]
    space_id = div["data-space-id"]

    commentURL = "https://news.yahoo.co.jp/comment/plugin/v1/full/?&sort=lost_points&order=desc&page=1&type=1"
    commentURL += "&full_page_url="+full_page_url+"&topic_id="+topic_id+"&space_id="+space_id
    return JsonResponse({"url":commentURL})

@require_POST
@csrf_exempt
def post_url(request):
    url = request.POST["url"]
    context={"message": "POST request received", "url": url}
    return JsonResponse(context)

@require_POST
@csrf_exempt
def collect_comments(request):

    url = request.POST["url"]
    if not "comments" in url:
        url+="/comments"
    res = requests.get(url)

    soup=BeautifulSoup(res.text, "html.parser")
    div = soup.find("div", {"class": "news-comment-plugin"})
    full_page_url = div["data-full-page-url"]
    topic_id = div["data-topic-id"]
    space_id = div["data-space-id"]
    commentURL = "https://news.yahoo.co.jp/comment/plugin/v1/full/?&sort=lost_points&order=desc&page=1&type=1"
    commentURL += "&full_page_url="+full_page_url+"&topic_id="+topic_id+"&space_id="+space_id

    res = requests.get(commentURL)
    soup=BeautifulSoup(res.text, "html.parser")
    commentItems = soup.find_all("li", {"class": "commentListItem"})
    data=[]
    for commentItem in commentItems:
        try:
            comment = commentItem.find("span", {"class": "cmtBody"}).text
            gotGood = commentItem.find("a", {"class": "agreeBtn"}).find("span", {"class": "userNum"}).text
            gotBad= commentItem.find("a", {"class": "disagreeBtn"}).find("span", {"class": "userNum"}).text
            data.append({"comment":comment, "good":gotGood, "bad":gotBad})
        except Exception:
            pass
    return JsonResponse({"data":data})