from .models import User

def create_user_service(data):
    try:
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            phone=data['phone'],
            gender=data['gender'],
            image=data['image'],
        )
        print(f"Creating user with data: {data}")


        if 'group' in data and data['group']:
            user.groups.add(data['group'])

        return user
    except Exception as e:
        return None

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
        user.password = data.get('password', user.password)
        user.phone = data.get('phone', user.phone)
        user.gender = data.get('gender', user.gender)
        user.image = data.get('image', user.image)

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
