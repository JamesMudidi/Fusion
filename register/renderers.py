from register.models import Registration, RegistrationEnquiry
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from rest_framework.utils.serializer_helpers import ReturnDict
import json
from rest_framework.renderers import JSONRenderer


class RegistrationJSONRenderer(JSONRenderer):
    """Properly render the responses for property views.
    Note that errors are not handled by the renderer but instead
    handled by default DRF exception handlers."""
    charset = 'utf-8'

    def single_registration_format(self, data):
        """When returning users, fields choices should be returned
        as human readable values.
        For example, instead or returning `shirt_size` as `S`,
        we should return `Small`"""

        # We should only format responses. Because reqeusts don't have
        # the `id` we skip all requests
        if data.get('id'):
            instance = Registration.objects.get(pk=data.get('id'))
            data['educationLevel'] = instance.get_educationLevel_display(
            ).title()
            data['shirtSize'] = instance.get_shirtSize_display(
            ).title()
            client = instance.client
            client_data = {
                'id': client.id,
                'client_name': client.client_name,
                'phone': client.phone,
                'email': client.email,
                'address': client.address,
                'admin_email': client.client_admin.email,
                'admin_id': client.client_admin.id
            }
            data['client'] = client_data

    def render(self, data, media_type=None, renderer_context=None):
        if isinstance(data, dict):

            errors = data.get('errors')

            if errors:
                return super().render(data)

            if type(data) == ReturnDict or type(data) == dict:
                # if the response has a `data` key, we pass the actual
                # payload to be rendered as the values in the `user`.
                try:
                    payload = data.get('data')['user']
                    if payload:
                        self.single_registration_format(payload)

                    return json.dumps(data)
                except TypeError:
                    return json.dumps(data)

            results = data.get('results')

            # when getting multiple items, the actual payload is contained
            # in the `results` key because they will be paginated
            if isinstance(results, list):
                for item in results:
                    self.single_registration_format(item)
                return json.dumps({
                    'data': {'users': data}
                })

        return json.dumps({
            'data': {'users': data}
        })


class RegistrationEnquiryJSONRenderer(JSONRenderer):
    """
    renderer for user enquiry for properly handling responses and 
    data that is returned
    """
    charset = "utf-8"

    def render(self, data, media_type=None, renderer_context=None):

        if isinstance(data, dict):
            errors = data.get('errors', None)

            if errors:
                return super().render(data)

            if 'ErrorDetail' in str(data):
                return json.dumps({
                    'errors': data}
                )

        return json.dumps({"data": {"enquiry": data}})