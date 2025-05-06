from ..users.authentication import get_authorization_header
# ------------------------------------- HELPER FUNCTION --------------------------------------
def get_token(request):
    auth_header = get_authorization_header(request).decode('utf-8')
    token = auth_header.replace('Bearer ', '') if auth_header and auth_header.startswith('Bearer ') else None
    return token