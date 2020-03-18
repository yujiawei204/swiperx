from qiniu import Auth, put_file

from swiper import cfg

def upload_to_qn(filename, filepath):
    '''将文件上传到七牛云'''

    # 构建鉴权对象
    qn_auth = Auth(cfg.QN_ACCESS_KEY, cfg.QN_SECRET_KEY)

    # 生成上传 Token，可以指定过期时间等
    token = qn_auth.upload_token(cfg.QN_BUCKET, filename, 3600)

    # 要上传文件的本地路径
    ret, info = put_file(token, filename, filepath)

    url = '%s/%s' % (cfg.QN_BASE_URL, filename)
    return url