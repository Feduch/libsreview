from allauth.account.adapter import DefaultAccountAdapter


class LibsAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_redirect_url(self, request):
        path = "/accounts/profile"
        return path
