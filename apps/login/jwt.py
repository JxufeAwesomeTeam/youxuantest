import python_jwt as jwt ,jwcrypto.jwk as jwk ,datetime
from django.http import HttpResponse


LIFE_TIME = 24 #小时

def update_pem():
    KEY = jwk.JWK.generate(kty='RSA', size=2048)

    PRIV_PEM = KEY.export_to_pem(private_key=True, password=None)
    PUB_PEM = KEY.export_to_pem()

    f1 = open('./PRIV.pem','wb')
    f2 = open('./PUB.pem','wb')

    f1.write(PRIV_PEM)
    f2.write(PUB_PEM)

    f1.close()
    f2.close()

def set_token(payload):
    f1 = open('apps/login/pem/PRIV.pem', 'rb')
    PRIV_PEM = f1.read()
    PRIV_KEY = jwk.JWK.from_pem(PRIV_PEM)  # 私密秘钥
    f1.close()
    #若payload不是dict类型的则返回None
    if isinstance(payload,dict):
        token = jwt.generate_jwt(payload,priv_key=PRIV_KEY,algorithm='RS256',lifetime=datetime.timedelta(hours=LIFE_TIME))
        return token

def get_token(request):
    try:
        AUTHORIZATION = request.META['HTTP_AUTHORIZATION'].split()
        if AUTHORIZATION[0] =='Token':
            token = AUTHORIZATION[1]
            return token
    except:
        pass


def verify_token(request):
    f2 = open('apps/login/pem/PUB.pem', 'rb')
    PUB_PEM = f2.read()
    PUB_KEY = jwk.JWK.from_pem(PUB_PEM)  # 公共秘钥
    f2.close()

    token = get_token(request)
    if token:
        try:
            header, claims = jwt.verify_jwt(token, pub_key=PUB_KEY, allowed_algs=['RS256'])
        except:
            raise Exception('请重新登录')
        else:
            uid = claims['uid']
        return int(uid)
    else:
        raise Exception('请使用Token验证登录')