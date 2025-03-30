from django.http import JsonResponse

def success_response(message, data=None, status=200):
    return JsonResponse({
        "status": "success",
        "message": message,
        "data": data,
    }, status=status)

def error_response(message, status=400):
    return JsonResponse({
        "status": "error",
        "message": message,
    }, status=status)