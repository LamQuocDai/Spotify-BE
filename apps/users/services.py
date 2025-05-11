from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .models import User
from django.contrib.auth.hashers import make_password
from .aws_helper import UserS3Uploader
import logging

logger = logging.getLogger(__name__)

def create_user_service(data, image_file=None):
    try:
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Missing required field: {field}")

        # Create the user with required fields
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

        # Handle image upload to AWS if provided
        if image_file:
            s3_uploader = UserS3Uploader()
            image_url = s3_uploader.upload_file(image_file, 'profiles')
            if image_url:
                user.image = image_url
            else:
                logger.error("Failed to upload profile image to S3")
                raise ValueError("Failed to upload profile image")
        elif 'image' in data and data['image']:
            user.image = data['image']

        # Save the changes
        user.save()

        # Add to group if specified
        if 'group' in data and data['group']:
            user.groups.add(data['group'])

        return user
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        raise

def get_users_service(page=1, page_size=10):
    try:
        users = User.objects.all().order_by('id')
        paginator = Paginator(users, page_size)
        try:
            paginated_users = paginator.page(page)
        except PageNotAnInteger:
            paginated_users = paginator.page(1)
        except EmptyPage:
            paginated_users = paginator.page(paginator.num_pages)

        users_data = [
            {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'gender': user.gender,
                'image': user.image,
                'status': user.status,
            }
            for user in paginated_users
        ]

        return {
            'users': users_data,
            'page': page,
            'page_size': page_size,
            'total_pages': paginator.num_pages,
            'total_users': paginator.count
        }
    except Exception as e:
        print(f"Error retrieving users: {str(e)}")
        raise

def get_user_service(user_id):
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return None
    except User.MultipleObjectsReturned:
        return None

def update_user_service(user_id, data, image_file=None):
    try:
        user = User.objects.get(id=user_id)

        # Update basic fields
        user.username = data.get('username', user.username)
        if 'password' in data and data['password']:
            user.password = make_password(data['password'])
        user.phone = data.get('phone', user.phone)
        user.gender = data.get('gender', user.gender)
        # Handle image upload to AWS if provided
        if image_file:
            s3_uploader = UserS3Uploader()

            # Delete old image if it exists
            if user.image and isinstance(user.image, str) and 'profiles/' in user.image:
                try:
                    s3_uploader.delete_file(user.image)
                except Exception as e:
                    logger.warning(f"Error deleting old profile image: {str(e)}")

            # Upload new image
            print(image_file)
            image_url = s3_uploader.upload_file(image_file)
            print(2)
            if image_url:
                user.image = image_url
            else:
                logger.error("Failed to upload profile image to S3")
                raise ValueError("Failed to upload profile image")
        elif 'image' in data:  # Only update if explicitly provided in data
            user.image = data['image']
        print(3)

        user.save()
        return user
    except User.DoesNotExist:
        return None
    except User.MultipleObjectsReturned:
        return None

def delete_user_service(user_id):
    try:
        user = User.objects.get(id=user_id)

        # Delete profile image from S3 if exists
        if user.image and isinstance(user.image, str) and 'profiles/' in user.image:
            try:
                s3_uploader = UserS3Uploader()
                s3_uploader.delete_file(user.image)
            except Exception as e:
                logger.warning(f"Error deleting user profile image: {str(e)}")
        user.delete()
        return user
    except User.DoesNotExist:
        return None
    except User.MultipleObjectsReturned:
        return None

def search_users_service(query, page=1, page_size=10):
    try:
        print(f"Search Query: '{query}'")  # Add for debugging
        users = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        ).order_by('id')
        print(f"Found {users.count()} users")  # Add for debugging
        paginator = Paginator(users, page_size)
        try:
            paginated_users = paginator.page(page)
        except PageNotAnInteger:
            paginated_users = paginator.page(1)
        except EmptyPage:
            paginated_users = paginator.page(paginator.num_pages)
        users_data = [
            {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'phone': user.phone,
                'gender': user.gender,
                'image': user.image,
                'status': user.status,
            }
            for user in paginated_users
        ]
        return {
            'users': users_data,
            'page': page,
            'page_size': page_size,
            'total_pages': paginator.num_pages,
            'total_users': paginator.count
        }
    except Exception as e:
        print(f"Error searching users: {str(e)}")
        raise