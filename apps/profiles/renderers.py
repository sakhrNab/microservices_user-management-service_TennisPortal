import json

from rest_framework.renderers import JSONRenderer


class ProfileJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    # a function which overrides render to render our profile
    def render(self, data, accepted_media_type=None, renderer_context=None):
        errors = data.get('errors', None)

        if errors is not None:
            return super(ProfileJSONRenderer, self).render(data)

        # render the profile using the name_space
        # whenever we use this renderer, we go to our profile
        # and get our data
        return json.dumps({"profile": data})