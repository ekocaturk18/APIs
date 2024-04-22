import json
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
import openai
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def a(request):
    if request.method == 'GET':
        API_KEY = open("API_KEY.txt",'r').read()
        story_content = open("SYSTEM_CONTENT.txt", 'r').read()
        openai.api_key = API_KEY
        chat_log = []
        chat_log.append({'role': 'system', 'content': story_content})
        chat_log.append({'role' : 'user', 'content': "Start the story"})
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = chat_log
        )
        ai_response = response['choices'][0]['message']['content']
        ai_response = ai_response.strip('/n').strip()
        chat_log.append({'role': 'assistant', 'content': ai_response})
        return HttpResponse(ai_response)
    else:
        return HttpResponse("empty")

@csrf_exempt
def b(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        messages = data.get('Messages', [])

        API_KEY = open("API_KEY.txt",'r').read()
        story_content = open("SYSTEM_CONTENT.txt", 'r').read()
        openai.api_key = API_KEY
        chat_log = []
        chat_log.append({'role': 'system', 'content': story_content})
        chat_log.append({'role': 'user', 'content': "Start the story"})

        for message in messages:
            if message["UserID"] == "ChatGPT":
                chat_log.append({'role': 'assistant', 'content': message["Content"]})
            else:
                chat_log.append({'role': 'user', 'content': message["Content"]})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_log
        )

        ai_response = response['choices'][0]['message']['content']
        ai_response = ai_response.strip('/n').strip()
        chat_log.append({'role': 'assistant', 'content': ai_response})
        return JsonResponse({"response": ai_response})
    else:
        return HttpResponse({"error": "Unsupported method"}, status=405)