#!/usr/bin/python

import string,re

name = "common-misspell"

import localeutil
e = localeutil.eucstr

# 의존명사를 위한 -할 형태의 동사 모음
verbs_re = "("+string.join([
    "가져올",
    "갈",
    "걸",
    "고칠"
    "나타날",
    "내릴",
    "놓일",
    "되돌릴",
    "만들",
    "바꿀",
    "보낼",
    "볼",
    "생길",
    "시킬",
    "쓸",
    "알",
    "얻어낼",
    "얻을",
    "없앨",
    "열",
    "올",
    "일",
    "읽어들일",
    "읽을",
    "있을",
    "잠글",
    "지울",
    "찾을",
    "할",
    ], '|')+")"

variations_re = "(있다|없다|있습니다|없습니다|있는|없는|있게|없게)"

# 조사 모음
chosa_re = "("+string.join([
    '가','이','이(가)',
    '를','을','을(를)',
    '는','은','은(는)',
    '로','으로','(으)로',
    '로서','으로서','(으)로서',
    '로써','으로써','(으)로써',
    '로부터','으로부터','(으)로부터',
    '라는','이라는','(이)라는',
    '의', '도', '에', '에서', '만', '부터',
    ], '|')+")"

misspell_data = [
    { 're':    re.compile(e("(않\s*(한|함|합니다|된|됨|됩니다))")),
      'error': e("\"%s\": 짧은 부정문에서는 '않'이 아니라 '안'을 씁니다") },
    { 're':    re.compile(e("(읍니다)")),
      'error': e("\"%s\": '읍니다'가 아니라 '습니다'입니다") },
    { 're':    re.compile(e("((없|있|남았)슴)")),
      'error': e("\"%s\": '슴'이 아니라 '음'입니다") },
    { 're':    re.compile(e("("+verbs_re+"수(가|도|는)?\s"+")")),
      'error': e("\"%s\": 의존 명사는 띄어 써야 합니다") },
    { 're':    re.compile(e("("+verbs_re+"\s*수(있|없)"+")")),
      'error': e("\"%s\": 의존 명사는 띄어 써야 합니다") },
    { 're':    re.compile(e("("+verbs_re+"때(가|도|는)?\s"+")")),
      'error': e("\"%s\": `~할 때'라고 띄어 써야 합니다") },
    { 're':    re.compile(e("([A-Za-z0-9-\._()%`'\"]+\s+"+chosa_re+")\s+")),
      'error': e("\"%s\": 조사는 체언에 붙여 써야 합니다") },
]

def check(msgid,msgstr):
    ret = 1
    errmsg = ""
    for data in misspell_data:
        misspell_re = data['re']
        misspell_error = data['error']
        str = msgstr
        while 1:
            mo = misspell_re.search(str)
            if mo:
                ret = 0
                if errmsg:
                    errmsg += '\n'
                errmsg += misspell_error % str[mo.start(1):mo.end(1)]
                str = str[mo.end():]
            else:
                break;
    return (ret, errmsg)    

if __name__ == '__main__':
    import sys
    msgid = sys.stdin.readline()
    msgstr = sys.stdin.readline()
    t,e = check(msgid,msgstr)
    if not t:
        print e
    else:
        print "Success"
