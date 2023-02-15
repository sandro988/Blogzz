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
        default="profile_pictures/default_profile_picture.webp",
    )

    def save(self, *args, **kwargs):
        "If user decides to delete their profile picture, it will automatically be set to default picture."
        if not self.profile_picture:
            self.profile_picture = "profile_pictures/default_profile_picture.webp"
        super().save(*args, **kwargs)

    def get_profile_picture(self):

        """
        Function created to return the profile picture URL for a user, profile picture will be either from their social account or from media folder.

        If user has signed up with google or github social accounts and they have not yet changed their profile picture, this function
        will return their social account profile picture URL from the first linked social account. For github account it gets the picture URL from
        extra_data['avatar_url'] and for google it gets the image from extra_data['picture'].

        But if the user has not signed up with social account this function will return either the default picture URL or the URL of a picture that
        the user has uploaded by themselves.

        Returns:
            str: The profile picture URL.
        """
        social_accounts = self.socialaccount_set.all()

        if (
            social_accounts
            and self.profile_picture == "profile_pictures/default_profile_picture.webp"
        ):
            social_account = social_accounts[0]

            if social_account.provider == "github":
                social_account_picture = social_account.extra_data["avatar_url"]
            else:
                social_account_picture = social_account.extra_data["picture"]

            return social_account_picture

        else:
            return self.profile_picture.url
