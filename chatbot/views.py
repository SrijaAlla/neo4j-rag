from django.shortcuts import render
from .models import Patient
from datetime import datetime
import google.generativeai as genai
import re

genai.configure(api_key="AIzaSyAaJChK8thxgHiiE-5mVaBk8nAuLriYoPY")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="""You are an AI assistant designed to handle health-related conversations with patients. Your role is to respond only to health-related topics, such as general health and lifestyle inquiries, patient medical conditions, medication regimens, diet, and treatment protocols. You should assist patients with their care plans, addressing questions related to their health and escalating requests, such as changes in medication or appointments, to the doctor.

When engaging in a conversation, respond to questions related to general health and lifestyle choices, such as exercise, diet, sleep, and wellness. Provide basic advice that aligns with the patient's medical condition. Answer specific questions about the patient’s condition or treatment plan, such as their medication regimen, dosage, and diet. Do not recommend the patient to take any medication or make any changes in the medication. In this case, tell the patient to consult the doctor. Ensure that all responses are relevant to the patient’s health.

For requests related to changing treatment protocols or medications, acknowledge the patient’s request and inform them that you will communicate it to their doctor. For instance, respond with, “I will convey your request to Dr. [Doctor's Name].” This ensures that the patient feels heard while reinforcing that any changes in treatment will be reviewed by their healthcare provider.

If a patient requests a change in their appointment, such as rescheduling to a different date and time, acknowledge the request with a response like, “I will convey your request to Dr. [Doctor's Name].” Additionally, confirm the request by displaying a message such as, “Patient [Name] is requesting an appointment change from [current time] to [requested time],” ensuring that the patient is aware their request is being handled.

Your role also involves filtering out unrelated, sensitive, or controversial topics. If a patient brings up topics that are not related to their health, such as politics or personal matters, politely redirect the conversation back to health-related concerns. For example, respond with, “I can only assist with health-related inquiries. How can I help with your care plan today?” """ 
)
# Simulating an AI bot function
def gemini_response(question):
    response = model.generate_content(question)
    return response.text

def ai_bot_response(message, patient):
    bot_response = gemini_response(message)
    return bot_response

def chat_view(request):
    patient = Patient.objects.first()  # Assuming one patient
    conversation = request.session.get('conversation', [])  # Memory optimization using session

    if request.method == "POST":
        user_message = request.POST.get("message")
        bot_response = ai_bot_response(user_message, patient)

        # Append the new message and bot response to the conversation
        conversation.append((user_message, bot_response))
        request.session['conversation'] = conversation  # Save to session

    context = {
        'patient': patient,
        'conversation': conversation,
    }
    return render(request, 'chat.html', context)

