from celery import shared_task
from . import services
from django.contrib.auth.models import User
from api.models import PestDiagnosis
from django.core.files.storage import default_storage
import os

@shared_task
def diagnose_task(crop_type: str, symptoms: str):
    return services.diagnose(crop_type, symptoms)

@shared_task
def farming_advice_task(lat: float, lng: float, crop_type: str, season: str):
    return services.farming_advice(lat, lng, crop_type, season)

@shared_task
def market_analysis_task(crop_type: str, district: str, quantity: float):
    return services.market_analysis(crop_type, district, quantity)

@shared_task
def async_pest_diagnosis(user_id: int, crop_type: str, symptoms: str, image_path: str):
    """
    Async task for pest diagnosis that processes the image and updates the diagnosis
    """
    try:
        user = User.objects.get(id=user_id)
        
        # Get the image file from storage
        if default_storage.exists(image_path):
            with default_storage.open(image_path, 'rb') as f:
                # Process the diagnosis
                diagnosis_result = services.diagnose_pest(crop_type, symptoms, f)
                
                # Update the existing PestDiagnosis record
                pest_diagnosis = PestDiagnosis.objects.filter(
                    user=user,
                    crop_type=crop_type,
                    symptoms=symptoms
                ).order_by('-created_at').first()
                
                if pest_diagnosis:
                    pest_diagnosis.diagnosis = diagnosis_result['diagnosis']
                    pest_diagnosis.confidence_score = diagnosis_result['confidence']
                    pest_diagnosis.treatment_advice = diagnosis_result['treatment']
                    pest_diagnosis.save()
                
                return {
                    'status': 'SUCCESS',
                    'diagnosis': diagnosis_result['diagnosis'],
                    'confidence': diagnosis_result['confidence'],
                    'treatment': diagnosis_result['treatment']
                }
        else:
            return {
                'status': 'ERROR',
                'error': 'Image file not found'
            }
            
    except Exception as e:
        return {
            'status': 'ERROR',
            'error': str(e)
        }
