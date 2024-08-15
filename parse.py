def get_captha(img_path: str, api_key):
    import os

    from twocaptcha import TwoCaptcha

    key = os.getenv('APIKEY_2CAPTCHA', api_key)

    solver = TwoCaptcha(key)

    try:
        result = solver.normal(img_path)
        return result['code']

    except Exception as e:
        print(e)