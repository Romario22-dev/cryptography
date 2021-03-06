# This file is dual licensed under the terms of the Apache License, Version
# 2.0, and the BSD License. See the LICENSE file in the root of this repository
# for complete details.


import base64
import typing
from urllib.parse import quote, urlencode


def _generate_uri(
    hotp,
    type_name: str,
    account_name: str,
    issuer: typing.Optional[str],
    extra_parameters,
):
    parameters = [
        ("digits", hotp._length),
        ("secret", base64.b32encode(hotp._key)),
        ("algorithm", hotp._algorithm.name.upper()),
    ]

    if issuer is not None:
        parameters.append(("issuer", issuer))

    parameters.extend(extra_parameters)

    uriparts = {
        "type": type_name,
        "label": (
            "%s:%s" % (quote(issuer), quote(account_name))
            if issuer
            else quote(account_name)
        ),
        "parameters": urlencode(parameters),
    }
    return "otpauth://{type}/{label}?{parameters}".format(**uriparts)
