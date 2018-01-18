from django.conf import settings
from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client


class FDFSStorage(Storage):
    """FDFS文件存储类"""

    def __init__(self, client_conf=None, nginx_url=None):
        """初始化"""
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = client_conf

        if nginx_url is None:
            nginx_url = settings.FDFS_NGINX_URL
        self.nginx_url = nginx_url

    def _open(self, name, mode='rb'):
        """打开文件时调用"""
        pass

    def _save(self, name, content):
        """保存文件时调用"""

        # name: 上传文件的名称
        # content: 包含上传文件内容的File类的实例对象

        # 创建一个Fdfs_client类的对象
        client = Fdfs_client(self.client_conf)
        # 上传文件到FDFS系统中
        # 获取上传文件内容
        content = content.read()

        # {
        #     'Group name': group_name,
        #     'Remote file_id': remote_file_id, # 返回的文件ID
        #     'Status': 'Upload successed.',
        #     'Local file name': '',
        #     'Uploaded size': upload_size,
        #     'Storage IP': storage_ip
        # } if success else None
        response = client.upload_by_buffer(content)

        if response is None or response.get('Status') != 'Upload successed.':
            raise Exception('上传文件到FDFS系统失败')

        file_id = response.get('Remote file_id')
        return file_id

    def exists(self, name):
        """判断文件是否存在"""
        return False

    def url(self, name):
        """返回可访问到文件的url路径"""
        return self.nginx_url + name
