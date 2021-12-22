import pyotp


def get_two_factor_auth_code(totp):
    totp = pyotp.TOTP(totp)
    return totp.now()


if __name__ == "__main__":
    print(get_two_factor_auth_code())
