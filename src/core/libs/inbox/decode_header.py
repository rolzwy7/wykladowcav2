# pylint: disable=unused-variable
# pylint: disable=broad-exception-caught
# pylint: disable=broad-exception-raised
# flake8: noqa:F841

from email.header import decode_header as _decode_header

from chardet import detect as chardet_detect


def decode_header(subject: str):
    """Decode header"""

    subject_parts = []
    for subject_part, email_encoding in _decode_header(subject):
        # Handle not encoded
        if email_encoding is None and not isinstance(subject_part, bytes):
            subject_parts.append(subject_part)
            continue

        # Apply detected encoding
        if email_encoding is not None:
            try:
                part = str(subject_part, email_encoding)
            except Exception as exception:
                pass
            else:
                subject_parts.append(part)
                continue

        # Try to blindly utf8 decode
        try:
            part = str(subject_part, "utf8")
        except Exception as exception:
            pass
        else:
            subject_parts.append(part)
            continue

        # Try chardet
        try:
            chardet_result = chardet_detect(subject_part)
            encoding = chardet_result["encoding"]
            if encoding:
                part = str(subject_part, encoding)
            else:
                raise Exception("Encoding is None")
        except Exception as exception:
            pass
        else:
            subject_parts.append(part)
            continue

        # Just give up and append string representation
        try:
            part = repr(subject_part)
        except Exception as exception:
            pass
        else:
            subject_parts.append(part)
            continue

    return (
        " ".join(subject_parts).strip().replace("\n", "").replace(" " * 2, " ")
    )
