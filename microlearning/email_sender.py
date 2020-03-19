from microlearning.models import Profile

category_users = {}
for profile in Profile.objects.all():
    if profile.subscribed_category:
        category_users.setdefault(profile.subscribed_category, []).append(profile.user.email)

