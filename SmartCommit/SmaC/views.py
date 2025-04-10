from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
from dotenv import load_dotenv
from google import generativeai as genai
from django.utils.timezone import now
# from django.contrib.auth import authenticate, login as auth_login
# from django.contrib.auth.models import User
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from dotenv import load_dotenv
from pathlib import Path

# env_path = Path(__file__).resolve().parent.parent / '.env'
# load_dotenv(dotenv_path=env_path)


# Load .env API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# System instruction
system_instruction = """"
You are a helpful and experienced code reviewer assistant.

Your task is to review a code snippet provided by the user.

You must return your review under the following six bullet-point sections, each separated clearly:

- Highlights
- Errors
- Suggestions
- Time Complexity
- Space Complexity
- Improvisation

Do not include any introductions, conclusions, emojis, or casual chat. Only return the review under these exact headings in clean markdown format.Do not mention yourself or introduce yourself , keep yourself also anonymous.
"""


@api_view(['POST'])
def ask_gemini(request):
    prompt = request.data.get("prompt", "")

    if not prompt:
        return Response({"error": "Prompt is required"}, status=400)

    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",  # Or gemini-pro
            system_instruction=system_instruction
        )

        response = model.generate_content(prompt)
        return Response({"reply": response.text})

    except Exception as e:
        return Response({"error": "Gemini API call failed", "details": str(e)}, status=500)

# @api_view(['POST'])
# def ask_gemini(request):
#     full_prompt = request.data.get("prompt", "")

#     if not full_prompt:
#         return Response({"error": "Prompt is required"}, status=400)

#     try:
#         model = genai.GenerativeModel("gemini-2.0-flash")  # or "gemini-2.0-pro" if you want
#         convo = model.start_chat(history=[])
#         response = convo.send_message(full_prompt)
#         return Response({"reply": response.text})
#     except Exception as e:
#         return Response({"error": "Gemini API call failed", "details": str(e)}, status=500)


# Create your views here.
def home(request):
 return render(request, 'home.html')


def terminal(request):
    return render(request, 'Terminal.html', {
        'timestamp': now().timestamp()  # this adds a unique query param to bust cache
    })

