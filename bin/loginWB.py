def login(self):
     # step-1. prelogin
     pre_login = self.prelogin()
     su = self.encrypt_user(self.weibo_user)
     sp = self.encrypt_passwd(
     self.weibo_password,
     pre_login['pubkey'],
     pre_login['servertime'],
     pre_login['nonce']
     )
     prelt = self.get_prelt(pre_login)
     data = {
         'entry': 'weibo',
         'gateway': 1,
         'from': '',
         'savestate': 7,
         'qrcode_flag': 'false',
         'userticket': 1,
         'pagerefer': '',
         'vsnf': 1,
         'su': su,
         'service': 'miniblog',
         'servertime': pre_login['servertime'],
         'nonce': pre_login['nonce'],
         'vsnf': 1,
         'pwencode': 'rsa2',
         'sp': sp,
         'rsakv' : pre_login['rsakv'],
         'encoding': 'UTF-8',
         'prelt': prelt,
         'sr': '1280*800',
         'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.',
         'sinaSSOController.feedBackUrlCallBack',
         'returntype': 'META'}
     # step-2 login POST
     login_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
     resp = self.session.post(login_url, data=data)
     print(resp.headers)
     print(resp.content)
     print('Step-2 response:', resp.text)
     # step-3 follow redirect
     redirect_url = re.findall(r'location\.replace\('(.*?)'', resp.text)[0]
     print('Step-3 to redirect:', redirect_url)
     resp = self.session.get(redirect_url)
     print('Step-3 response:', resp.text)
     # step-4 process step-3's response
     arrURL = re.findall(r''arrURL':(.*?)\}', resp.text)[0]
     arrURL = json.loads(arrURL)
     print('CrossDomainUrl:', arrURL)
     for url in arrURL:
     print('set CrossDomainUrl:', url)
     resp_cross = self.session.get(url)
     print(resp_cross.text)
     redirect_url = re.findall(r'location\.replace\(\'(.*?)\'', resp.text)[0]
     print('Step-4 redirect_url:', redirect_url)
     resp = self.session.get(redirect_url)
     print(resp.text)
     with open(self.cookies_tosave, 'wb') as f:
     pickle.dump(self.session.cookies, f)
     return True