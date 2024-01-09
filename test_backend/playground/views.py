from django.shortcuts import render
from django.http import HttpResponse, JsonResponse



def say_hello(request):
	data = [{
		"width": 10,
		"height": 5,
		"id": "dsfs3-sd"
	},
	{
		"width": 15,
		"height": 7,
		"id": "dsfs3-sd"
	},
	{
		"width": 1,
		"height": 2,
		"id": "dsfsds3-sd"
	}]
	response = JsonResponse(data, safe=False)
	return response