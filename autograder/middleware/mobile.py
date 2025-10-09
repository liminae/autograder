from django.shortcuts import redirect

EXCLUDED_PATHS = ["/mobile/", "/djangoadmin/", "/static/"]  # Add more if needed


class MobileRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip paths you don't want redirected
        if any(request.path.startswith(p) for p in EXCLUDED_PATHS):
            return self.get_response(request)

        # Use django-user-agents detection
        if hasattr(request, "user_agent") and request.user_agent.is_mobile:
            return redirect("/mobile/")  # Redirect mobile users

        return self.get_response(request)
