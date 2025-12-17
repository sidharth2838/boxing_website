import json
import openai
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.cache import cache
from django.conf import settings
from .models import BoxingFAQ, ChatHistory, TrainingSchedule, MembershipPlan

# Initialize OpenAI (you'll need to set OPENAI_API_KEY in settings)
openai.api_key = getattr(settings, 'OPENAI_API_KEY', '')

@csrf_exempt
@require_POST
def chatbot_api(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        user_id = data.get('user_id')
        
        if not user_message:
            return JsonResponse({'error': 'Empty message'}, status=400)
        
        # Check if user is authenticated
        user = request.user if request.user.is_authenticated else None
        
        # Step 1: Check if it's a boxing-related question using AI
        is_boxing_related = check_if_boxing_related(user_message)
        
        if not is_boxing_related:
            # Save to history as non-boxing related
            if user:
                ChatHistory.objects.create(
                    user=user,
                    user_message=user_message,
                    bot_response="I specialize in boxing-related questions only.",
                    is_boxing_related=False
                )
            return JsonResponse({
                'response': "I'm a boxing specialist assistant. I can only help with boxing-related questions like training, techniques, schedules, and equipment. Please ask me about boxing! 🥊"
            })
        
        # Step 2: Check database for FAQs first
        faq_response = get_faq_response(user_message)
        if faq_response:
            response_text = faq_response
        else:
            # Step 3: Check live data from database
            live_data_response = get_live_data_response(user_message)
            if live_data_response:
                response_text = live_data_response
            else:
                # Step 4: Use AI for boxing-specific response
                response_text = get_ai_boxing_response(user_message)
        
        # Save to chat history
        if user:
            ChatHistory.objects.create(
                user=user,
                user_message=user_message,
                bot_response=response_text,
                is_boxing_related=True
            )
        
        return JsonResponse({'response': response_text})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def check_if_boxing_related(message):
    """Use AI to determine if the question is boxing-related"""
    try:
        if not openai.api_key:
            # Fallback: simple keyword check if no API key
            boxing_keywords = [
                'boxing', 'punch', 'glove', 'train', 'spar', 'jab', 'cross', 'hook',
                'uppercut', 'heavy bag', 'speed bag', 'ring', 'round', 'coach',
                'training', 'technique', 'footwork', 'defense', 'combination',
                'knockout', 'referee', 'gym', 'membership', 'schedule', 'class'
            ]
            return any(keyword in message.lower() for keyword in boxing_keywords)
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Determine if this question is related to boxing, martial arts, training, fitness, or gym membership. Answer only 'yes' or 'no'."},
                {"role": "user", "content": f"Question: {message}"}
            ],
            max_tokens=10,
            temperature=0
        )
        
        answer = response.choices[0].message.content.strip().lower()
        return 'yes' in answer
        
    except Exception:
        # Fallback to keyword check if AI fails
        boxing_keywords = ['boxing', 'train', 'punch', 'glove', 'spar', 'gym', 'coach']
        return any(keyword in message.lower() for keyword in boxing_keywords)

def get_faq_response(message):
    """Check database FAQs for matching questions"""
    try:
        # Search in FAQs
        faqs = BoxingFAQ.objects.filter(is_active=True)
        for faq in faqs:
            keywords = [k.strip().lower() for k in faq.keywords.split(',')]
            if any(keyword in message.lower() for keyword in keywords):
                return faq.answer
        return None
    except Exception:
        return None

def get_live_data_response(message):
    """Fetch live data from database"""
    message_lower = message.lower()
    
    try:
        # Check for schedule-related questions
        if any(word in message_lower for word in ['schedule', 'time', 'when', 'class', 'training time']):
            schedules = TrainingSchedule.objects.all().order_by('day', 'time_slot')
            if schedules.exists():
                response = "📅 Current Training Schedule:\n\n"
                current_day = None
                for schedule in schedules:
                    if schedule.day != current_day:
                        response += f"\n{schedule.get_day_display()}:\n"
                        current_day = schedule.day
                    response += f"• {schedule.time_slot} - {schedule.class_type} (Coach: {schedule.coach}) - {schedule.available_slots} slots available\n"
                return response + "\nBook your spot through our website or front desk!"
        
        # Check for membership questions
        if any(word in message_lower for word in ['membership', 'price', 'cost', 'plan', 'fee']):
            plans = MembershipPlan.objects.filter(is_active=True)
            if plans.exists():
                response = "💳 Membership Plans:\n\n"
                for plan in plans:
                    response += f"• {plan.name}: ${plan.price}/{plan.duration}\n"
                    response += f"  Features: {plan.features}\n\n"
                return response + "Visit us for a free trial class!"
        
        # Check for coach information
        if any(word in message_lower for word in ['coach', 'trainer', 'instructor']):
            # Get unique coaches from schedule
            coaches = TrainingSchedule.objects.values_list('coach', flat=True).distinct()
            if coaches:
                return f"👨‍🏫 Our certified coaches: {', '.join(coaches)}\n\nAll our coaches are experienced professionals with competitive backgrounds. Book a private session for personalized training!"
        
        return None
        
    except Exception:
        return None

def get_ai_boxing_response(message):
    """Get AI response for boxing-specific questions"""
    try:
        if openai.api_key:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": """You are BoxingBot, an expert boxing assistant for BoxingPro gym. 
                    Only provide information about boxing training, techniques, equipment, and fitness.
                    If asked about non-boxing topics, politely redirect to boxing.
                    Keep responses concise and helpful. Include emojis occasionally.
                    Focus on practical boxing advice."""},
                    {"role": "user", "content": message}
                ],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        else:
            # Fallback responses if no AI key
            return "I'd love to help with boxing advice! For detailed AI-powered responses, please configure the OpenAI API key. Meanwhile, you can ask about our training schedules, membership plans, or boxing techniques! 🥊"
            
    except Exception as e:
        return f"I'm having trouble connecting to my AI service right now. Please try again later or ask about our training schedules and membership plans! 🥊"

# Additional API endpoints
@csrf_exempt
def get_training_schedule(request):
    """API to get training schedule"""
    schedules = TrainingSchedule.objects.all().order_by('day', 'time_slot')
    data = []
    for schedule in schedules:
        data.append({
            'day': schedule.get_day_display(),
            'time_slot': schedule.time_slot,
            'class_type': schedule.class_type,
            'coach': schedule.coach,
            'available_slots': schedule.available_slots
        })
    return JsonResponse({'schedules': data})

@csrf_exempt
def get_membership_plans(request):
    """API to get membership plans"""
    plans = MembershipPlan.objects.filter(is_active=True)
    data = []
    for plan in plans:
        data.append({
            'name': plan.name,
            'price': str(plan.price),
            'duration': plan.duration,
            'features': plan.features
        })
    return JsonResponse({'plans': data})