
# Local AI services - integrates transformer model if available, otherwise uses a small sklearn fallback.
from __future__ import annotations
from typing import Dict, Any
from . import transformer_model
# keep old sklearn-based fallback here
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from PIL import Image
import io

_fallback_model = None
_labels = {
    "leaf_blight": {"name":"Leaf Blight", "treatment":"Apply copper fungicide, remove debris, rotate crops."},
    "bacterial_wilt": {"name":"Bacterial Wilt", "treatment":"Remove infected plants, sanitize tools, use resistant varieties."},
    "powdery_mildew": {"name":"Powdery Mildew", "treatment":"Use sulfur sprays, improve airflow."},
    "nitrogen_deficiency": {"name":"Nitrogen Deficiency", "treatment":"Apply nitrogen fertilizer."},
}

def _ensure_fallback():
    global _fallback_model
    if _fallback_model is not None:
        return
    samples = [
        ("yellow leaves with brown spots", "leaf_blight"),
        ("brown circular lesions on leaves", "leaf_blight"),
        ("wilting plants and slimy stems", "bacterial_wilt"),
        ("sudden plant wilt during day recovers at night", "bacterial_wilt"),
        ("powdery white coating on leaves", "powdery_mildew"),
        ("white powder and leaf curling", "powdery_mildew"),
        ("stunted growth and yellowing lower leaves", "nitrogen_deficiency"),
        ("pale leaves, poor vigor", "nitrogen_deficiency"),
    ]
    X, y = zip(*samples)
    clf = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1,2))), ("nb", MultinomialNB())])
    clf.fit(X, y)
    _fallback_model = clf

def diagnose(crop_type: str, symptoms: str) -> Dict[str, Any]:
    # prefer transformer if available
    try:
        res = transformer_model.classify(symptoms)
        label = res.get('label', 'INCONCLUSIVE').lower()
        score = res.get('score', 0.0)
        # map some labels to our known labels best-effort
        if 'BLIGHT' in label.upper() or 'BLIGHT' in label:
            key = 'leaf_blight'
        elif 'WILT' in label.upper() or 'WILT' in label:
            key = 'bacterial_wilt'
        else:
            # fallback mapping
            key = label.lower()
        info = _labels.get(key, {"name":"Inconclusive","treatment":"Provide clearer photos."})
        return {"diagnosis": f"{crop_type.title()} - {info['name']}", "treatment": info['treatment'], "confidence": float(score)}
    except Exception:
        # fallback to sklearn
        _ensure_fallback()
        pred = _fallback_model.predict([symptoms])[0]
        proba = max(_fallback_model.predict_proba([symptoms])[0])
        info = _labels.get(pred, {"name":"Inconclusive","treatment":"Provide clearer photos."})
        return {"diagnosis": f"{crop_type.title()} - {info['name']}", "treatment": info['treatment'], "confidence": float(proba)}

def diagnose_pest(crop_type: str, symptoms: str, image) -> Dict[str, Any]:
    """
    Main function for pest diagnosis that integrates image analysis with symptom analysis
    """
    try:
        # Process the image if it's a file
        if hasattr(image, 'read'):
            # Convert image to PIL Image for analysis
            img = Image.open(image)
            # Basic image analysis could go here
            # For now, we'll use the symptoms-based diagnosis
        
        # Use the existing diagnose function
        result = diagnose(crop_type, symptoms)
        
        # Enhance with crop-specific advice
        crop_advice = get_crop_specific_advice(crop_type, result['diagnosis'])
        if crop_advice:
            result['treatment'] += f" {crop_advice}"
        
        return result
        
    except Exception as e:
        # Fallback to basic diagnosis
        return diagnose(crop_type, symptoms)

def get_crop_specific_advice(crop_type: str, diagnosis: str) -> str:
    """Provide crop-specific treatment advice"""
    crop_advice = {
        'maize': 'For maize, ensure proper spacing and avoid overhead irrigation.',
        'tomatoes': 'For tomatoes, use trellising and avoid wetting leaves.',
        'beans': 'For beans, practice crop rotation and use resistant varieties.',
        'rice': 'For rice, maintain proper water levels and use certified seeds.',
    }
    
    crop_lower = crop_type.lower()
    for crop, advice in crop_advice.items():
        if crop in crop_lower:
            return advice
    return ""

# farming_advice and market_analysis remain as in previous file
def farming_advice(lat: float, lng: float, crop_type: str, season: str):
    season = season.lower()
    if 'rain' in season:
        planting = 'Early November'
        advice = f"For {crop_type}, prepare ridges now and plant with first effective rains. Apply basal fertilizer."
    else:
        planting = 'Irrigated: stagger plantings every 2 weeks'
        advice = f"Use mulching and drip irrigation for {crop_type} during dry season."
    return {'advice': advice, 'plantingDate': planting}

def get_farming_advice(lat: float, lng: float, crop_type: str, season: str):
    """Wrapper function for farming advice"""
    return farming_advice(lat, lng, crop_type, season)

def market_analysis(crop_type: str, district: str, quantity: float):
    base_price = { 'maize': 350.0, 'rice': 900.0, 'beans': 800.0 }.get(crop_type.lower(), 500.0)
    district_adj = { 'lilongwe': 1.05, 'blantyre': 1.08, 'mzuzu': 0.98 }.get(district.lower(), 1.0)
    bulk_disc = 0.95 if quantity >= 1000 else (0.98 if quantity >= 200 else 1.0)
    predicted = base_price * district_adj * bulk_disc
    trend = 'rising' if district_adj > 1.03 else ('falling' if bulk_disc < 1.0 else 'stable')
    return {'predictedPrice': round(predicted, 2), 'trend': trend}

def analyze_market(crop_type: str, district: str, quantity: float):
    """Wrapper function for market analysis"""
    return market_analysis(crop_type, district, quantity)
