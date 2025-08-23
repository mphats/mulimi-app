import json
import time
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.db import connection
from .models import RequestLog

def user_or_ip(group, request):
    if request.user.is_authenticated:
        return f"user:{request.user.id}"
    # basic ip
    ip = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", ""))
    return f"ip:{ip}"

class AuditMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request._audit_start = time.time()

    def process_response(self, request, response):
        try:
            duration = int((time.time() - getattr(request, "_audit_start", time.time())) * 1000)
            if request.path.startswith("/api/"):
                body = getattr(request, "body", b"")[:4096]
                try:
                    req_json = json.loads(body.decode("utf-8") or "{}")
                except Exception:
                    req_json = {}
                resp_body = getattr(response, "content", b"")[:4096]
                try:
                    resp_json = json.loads(resp_body.decode("utf-8") or "{}")
                except Exception:
                    resp_json = {"non_json": True}
                RequestLog.objects.create(
                    endpoint=request.path,
                    request_body=req_json,
                    response_body={"status": response.status_code, "data": resp_json, "ms": duration}
                )
        except Exception:
            pass
        return response
