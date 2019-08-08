import re
from django.core.exceptions import ValidationError


def check_project_name(string):
    pattern = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if pattern.search(string) is not None:
        raise ValidationError(
            'Special Character Not Accepted',
            params={'value': string},
        )
