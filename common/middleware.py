from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from common import stat


class AuthMiddleware(MiddlewareMixin):
    '''登陆检查中间件'''
    API_WHITE_LIST = [
        '/user/get_vcode',
        '/user/submit_vcode'
    ]

    def process_request(self, request):
        if request.path in self.API_WHITE_LIST:
            return

        uid = request.session.get('uid')
        if not uid:
            return JsonResponse({'code': stat.LOGIN_REQUIRED, 'data': None})