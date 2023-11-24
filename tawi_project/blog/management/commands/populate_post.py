import requests
from django.core.management.base import BaseCommand
from users.models import CustomUser
from blog.models import post
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populate the post model with data from JSONPlaceholder API'

    def handle(self, *args, **options):
        # Fetch posts from the JSONPlaceholder API
        response = requests.get('https://jsonplaceholder.typicode.com/posts')
        posts_data = response.json()

        # Iterate through posts and create post objects
        for post_data in posts_data:
            # Assuming 'userId' in post_data represents the user ID
            user_id = post_data['userId']

            # Get or create the CustomUser object
            user, created = CustomUser.objects.get_or_create(id=user_id, defaults={'username': f'user{user_id}'})

            # Create the post object
            post.objects.create(
                title=post_data['title'],
                content=post_data['body'],
                author=user,
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated posts'))

