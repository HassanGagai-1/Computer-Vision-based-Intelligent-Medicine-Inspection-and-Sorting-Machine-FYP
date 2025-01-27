import pyotp

def generate_totp_secret():
    return pyotp.random_base32()

def get_totp_uri(secret, firstname, issuer='MyApp'):
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=firstname, issuer_name=issuer)


def verify_totp_code(secret, code):
    """Verify a TOTP code against a given secret."""
    totp = pyotp.TOTP(secret)
    return totp.verify(code)