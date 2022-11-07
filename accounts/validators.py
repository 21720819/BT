from django.core.exceptions import ValidationError

def validate_symbols(email):
    if ("@ynu.ac.kr" not in email):
        raise ValidationError("영남대학교 이메일을 사용해야합니다.", code = 'symbol-err')
        