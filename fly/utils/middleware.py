from threading import current_thread

class RequestContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 设置当前用户
        current_thread().current_user = request.user

        # 获取客户端信息
        current_thread().remote_addr = request.META.get('REMOTE_ADDR')
        current_thread().user_agent = request.headers.get('User-Agent')

        response = self.get_response(request)
        return response