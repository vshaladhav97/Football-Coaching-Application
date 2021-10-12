from django.http.response import HttpResponse, JsonResponse
from customer.models import User
from authentication.config import perms_config
from first_kick_management.settings import logger
import re


def format_path(raw_path, pk):
    """Format all kind of urls and send the finale path"""

    media_pdf = ['media', '.pdf', '.docx', '.mp4']
    path = raw_path.split("?=")[0]
    if pk or any(x in path for x in media_pdf):
        path = path.rsplit("/", 1)[0]
        logger.info(path)

        return path

    return path


def check_url_pass(path, view_function):
    """Check for urls pass without check for permissions"""

    if path in perms_config.pass_urls or 'django.contrib.admin' in view_function.__module__ or re.search(r"^/static/.*\.(css|js|svg|jpeg|jpg|png|woff)$", path) or re.search(r"^/reset/.*", path):
        return True
    return None


def check_url_pass_view(path):
    if path in perms_config.pass_urls:
        return True
    else:
        return False


def get_permission(request):
        try:
            user_id = request.user.id
            perms = User.objects.filter(
                id=user_id
            ).filter(
                role__role_status=True
            ).filter(
                role__permissions__status=True
            ).values(
                'role__permissions__permission_name',
                'role__permissions__api_method',
                'role__permissions__url_identifier')

            # Permissions setting in session
            perms_list_font_end = []
            permission_list_backend = []

            for perm in perms:
                permission_dict = {}
                for key, value in perm.items():
                    if key == 'role__permissions__permission_name':
                        permission_dict['permission_name'] = value.lower()

                    elif key == 'role__permissions__api_method':
                        permission_dict['api_method'] = value.lower()

                    else:
                        permission_dict['url_identifier'] = value

                perm_name_method = perm['role__permissions__permission_name'].lower(
                ) + '_' + perm['role__permissions__api_method'].lower()
                perms_list_font_end.append(perm_name_method)

                permission_list_backend.append(permission_dict)

            request.session[perms_config.session_perm_key] = permission_list_backend
            request.session.modified = True
        except Exception as e:
            logger.error(e, exc_info=True)
            return HttpResponse(403)


def set_permission(request, user):
    try:
        perms = User.objects.filter(
            id=user
        ).filter(
            role__role_status=True
        ).filter(
            role__permissions__status=True
        ).values(
            'role__permissions__permission_name',
            'role__permissions__api_method',
            'role__permissions__url_identifier')

        # Permissions setting in session
        perms_list_font_end = []
        permission_list_backend = []

        for perm in perms:
            permission_dict = {}
            for key, value in perm.items():
                if key == 'role__permissions__permission_name':
                    permission_dict['permission_name'] = value.lower()

                elif key == 'role__permissions__api_method':
                    permission_dict['api_method'] = value.lower()

                else:
                    permission_dict['url_identifier'] = value

            perm_name_method = perm['role__permissions__permission_name'].lower(
            ) + '_' + perm['role__permissions__api_method'].lower()
            perms_list_font_end.append(perm_name_method)

            permission_list_backend.append(permission_dict)

        request.session[perms_config.session_perm_key] = permission_list_backend
        request.session.modified = True
    except Exception as e:
        logger.error(e, exc_info=True)
        return HttpResponse(403)


def check_role_permission():
    """
    Decorder checks permission for requested url and method with session.
    """

    def inner(func):
        def wrap(self, request, *awargs, **kwargs):

            pk = kwargs.get('pk')

            # Exact url from the function
            raw_path = request.path
            path = format_path(raw_path, pk)

            # Exact method from the function
            method = request.method.lower()

            try:
                check_url_pass = check_url_pass_view(path)
                if check_url_pass:
                    return func(self, request, *awargs, **kwargs)

                # Get the Global Permission key
                get_session_perm_key = perms_config.session_perm_key

                if perms_config.session_perm_key in request.session:
                    pass
                else:
                    get_permission(request)

                # if get_session_perm_key in request.session:

                # Get permissions list value from the session
                session_perms_list = request.session[get_session_perm_key]
                # Looping through the list of session perms
                for session_perms in session_perms_list:
                    # Compare the method and path
                    if session_perms['api_method'] == method and session_perms['url_identifier'] == path:
                        return func(self, request, *awargs, **kwargs)
                return HttpResponse(status=403)

            except Exception as e:
                logger.error(e, exc_info=True)
                return HttpResponse(status=403)
        return wrap
    return inner

