from django.http import JsonResponse


class HttpResponseAjax(JsonResponse):
    def __init__(self, status="ok", **kwargs):
        kwargs["status"] = status
        super().__init__(kwargs)


class HttpResponseAjaxError(HttpResponseAjax):
    def __int__(self, code, message):
        super().__int__(
            status="error", code=code, message=message
        )


def login_required_ajax(view):
    def decorated_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view(request, *args, **kwargs)
        else:
            return HttpResponseAjaxError(
                code="no_auth",
                message="Требуется авторизация",
            )
    return decorated_view
