from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        data = request.data
        user.nickname = data.get('nickname', '')
        user.birth = data.get('birth')
        user.profile_img = data.get('profile_img')
        if commit:
            user.save()
        return user
