import pyotp
import qrcode
import io

def generate_totp_secret():
    return pyotp.random_base32()

def get_totp_uri(secret, firstname, issuer='MyApp'):
    """
    Generate a TOTP provisioning URI, which can be turned into a QR code
    the user can scan with Google Authenticator, Authy, etc.
    """
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=firstname, issuer_name=issuer)

def generate_qr_code_image(totp_uri):
    """Generate a QR code in memory (as PNG bytes) from the TOTP URI."""
    img = qrcode.make(totp_uri)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf
def verify_totp_code(secret, code):
    """Verify a TOTP code against a given secret."""
    totp = pyotp.TOTP(secret)
    return totp.verify(code)
