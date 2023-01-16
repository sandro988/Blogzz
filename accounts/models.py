from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToCover

class CustomUser(AbstractUser):
    profile_picture = ProcessedImageField(
        upload_to="profile_pictures/users",
        processors=[ResizeToCover(100, 100)],
        format="JPEG",
        options={"quality": 100},
        blank=True,
        default='profile_pictures/default_profile_picture.jpg'
    )

    def save(self, *args, **kwargs):
        "If user decides to delete their profile picture, it will automatically be set to default picture."
        if not self.profile_picture:
            self.profile_picture = 'profile_pictures/default_profile_picture.jpg'
        super().save(*args, **kwargs)
