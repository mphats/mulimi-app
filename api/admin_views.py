
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime
from .models import RequestLog
from .permissions import HasRole
from django.core.paginator import Paginator

@api_view(['GET'])
@permission_classes([IsAuthenticated, HasRole(['ADMIN'])])
def audit_logs(request):
    qs = RequestLog.objects.all().order_by('-created_at')
    endpoint = request.query_params.get('endpoint')
    if endpoint:
        qs = qs.filter(endpoint__icontains=endpoint)
    start = request.query_params.get('start')
    end = request.query_params.get('end')
    if start:
        dt = parse_datetime(start)
        if dt:
            qs = qs.filter(created_at__gte=dt)
    if end:
        dt = parse_datetime(end)
        if dt:
            qs = qs.filter(created_at__lte=dt)
    page = int(request.query_params.get('page', 1))
    per = int(request.query_params.get('per', 25))
    p = Paginator(qs, per)
    items = []
    for obj in p.get_page(page):
        items.append({'id': obj.id, 'endpoint': obj.endpoint, 'created_at': obj.created_at.isoformat(), 'request_body': obj.request_body, 'response_body': obj.response_body})
    return Response({'count': p.count, 'page': page, 'per': per, 'results': items})
