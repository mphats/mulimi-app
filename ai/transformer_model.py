
"""Transformer-backed classifier wrapper.
Tries to load a local or HuggingFace model for text-classification. If not available,
falls back to the scikit-learn pipeline inside services.py.
"""
from typing import Optional, Dict, Any

_model = None

def load_model(model_name: Optional[str] = None):
    global _model
    if _model is not None:
        return _model
    try:
        from transformers import pipeline
        # default: small distil model; user can replace with path to local checkpoint
        model_to_use = model_name or 'distilbert-base-uncased-finetuned-sst-2-english'
        _model = pipeline('text-classification', model=model_to_use, return_all_scores=False)
        return _model
    except Exception as e:
        # model missing; caller should fallback
        _model = None
        return None

def classify(text: str) -> Dict[str, Any]:
    mdl = load_model()
    if mdl is None:
        raise RuntimeError('transformer model not available')
    out = mdl(text)
    # pipeline returns list like [{'label':'POSITIVE','score':0.99}]
    if isinstance(out, list):
        o = out[0]
        return {'label': o.get('label'), 'score': float(o.get('score', 0.0))}
    else:
        return {'label': out.get('label'), 'score': float(out.get('score', 0.0))}
