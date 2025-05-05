from .models import User


def create_user_service(data):
    try:
        # Print the data being received to debug
        print(f"Creating user with data: {data}")

        # Validate required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Missing required field: {field}")

        # Create the user with only required fields first
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
        )

        # Add optional fields if they exist
        if 'phone' in data and data['phone']:
            user.phone = data['phone']

        if 'gender' in data and data['gender'] is not None:
            user.gender = data['gender']

        if 'image' in data and data['image']:
            user.image = data['image']

        # Save the changes
        user.save()

        # Add to group if specified
        if 'group' in data and data['group']:
            user.groups.add(data['group'])

        return user
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        raise  # Re-raise the exception instead of returning None

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
