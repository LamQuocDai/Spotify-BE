from .models import User

def create_user_service(data):
    user = User.objects.create(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    return user

def get_users_service():
    return list(User.objects.all().values())

def get_user_service(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return None
    except User.MultipleObjectsReturned:
        return None

def update_user_service(user_id, data):
    try:
        user = User.objects.get(id=user_id)
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.save()
        return user
    except User.DoesNotExist:
        return None
    except User.MultipleObjectsReturned:
        return None

def delete_user_service(user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return user
    except User.DoesNotExist:
        return None
    except User.MultipleObjectsReturned:
        return None
