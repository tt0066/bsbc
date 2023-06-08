import cv2
import numpy as np
import pywt
import hashlib
import phe
from phe import paillier
import json
from PIL import ImageFont, ImageDraw, Image


def keypair_dump_jwk(pub, priv, date=None):
    """Serializer for public-private keypair, to JWK format."""
    from datetime import datetime

    if date is None:
        date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    rec_pub = {
        "kty": "DAJ",
        "alg": "PAI-GN1",
        "key_ops": ["encrypt"],
        "n": phe.util.int_to_base64(pub.n),
        "kid": "Paillier public key generated by phe on {}".format(date),
    }

    rec_priv = {
        "kty": "DAJ",
        "key_ops": ["decrypt"],
        "p": phe.util.int_to_base64(priv.p),
        "q": phe.util.int_to_base64(priv.q),
        "kid": "Paillier private key generated by phe on {}".format(date),
    }

    priv_jwk = json.dumps(rec_priv)
    pub_jwk = json.dumps(rec_pub)
    return pub_jwk, priv_jwk


def seller_img_hash(img):
    """
    imput: image's absolute path
    output: string, image's hash
    """
    Hash = hashlib.md5(img).hexdigest()
    return "0x" + Hash


def buyer_gene_save_key(save_key_path):
    pub, priv = phe.generate_paillier_keypair()
    print("The public key is: ", pub)
    pub_jwk, priv_jwk = keypair_dump_jwk(pub, priv)
    with open(save_key_path + "\\public key.pub", "w") as f1:
        f1.write(pub_jwk + "\n")
        print("write public key to {0}\\public key.pub".format(save_key_path))
    with open(save_key_path + "\\privte key.priv", "w") as f2:
        f2.write(priv_jwk + "\n")
        print("write privte key to {0}\\privte key.priv".format(save_key_path))
    return pub, priv


def buyer_load_keypair(PublicKeyPath, PrivteKeyPath):
    with open(PublicKeyPath, "r+") as f1:
        pub_jwk = f1.read()
    with open(PrivteKeyPath, "r+") as f2:
        priv_jwk = f2.read()
    rec_pub = json.loads(pub_jwk)
    rec_priv = json.loads(priv_jwk)
    # Do some basic checks
    assert rec_pub["kty"] == "DAJ", "Invalid public key type"
    assert rec_pub["alg"] == "PAI-GN1", "Invalid public key algorithm"
    assert rec_priv["kty"] == "DAJ", "Invalid private key type"
    pub_n = phe.util.base64_to_int(rec_pub["n"])
    pub = paillier.PaillierPublicKey(pub_n)
    priv_p = phe.util.base64_to_int(rec_priv["p"])
    priv_q = phe.util.base64_to_int(rec_priv["q"])
    priv = paillier.PaillierPrivateKey(pub, priv_p, priv_q)
    return pub, priv


def seller_load_key(keypath):
    with open(keypath, "r+") as f:
        pub_jwk = f.read()
    rec_pub = json.loads(pub_jwk)
    assert rec_pub["kty"] == "DAJ", "Invalid public key type"
    assert rec_pub["alg"] == "PAI-GN1", "Invalid public key algorithm"
    pub_n = phe.util.base64_to_int(rec_pub["n"])
    pub = paillier.PaillierPublicKey(pub_n)
    return pub


def Arnold(img, key, a, b):
    r, c = img.shape[0], img.shape[1]
    p = np.zeros((r, c), np.uint8)
    for k in range(key):
        for i in range(r):
            for j in range(c):
                x = (i + b * j) % r
                y = (a * i + (a * b + 1) * j) % c
                p[x, y] = img[i, j]
    return p


def inverse_arnold(img, key, a, b):
    r = img.shape[0]
    c = img.shape[1]
    p = np.zeros((r, c), np.uint8)
    for k in range(key):
        for i in range(r):
            for j in range(c):
                x = ((a * b + 1) * i - b * j) % r
                y = (-a * i + j) % c
                p[x, y] = img[i, j]
    return p


def buyer_get_water(fontpath, addr: str, hash: str, key: int, a: int, b: int, SavePath):
    """
    input:public address, image's hash, secret parament:key,a,b,c,d
    return: nothing, save two images
    """
    add1 = addr[:16]
    add2 = addr[16:32]
    add3 = addr[32:]
    hash1 = hash[:17]
    hash2 = hash[17:34]
    hash3 = hash[34:]
    Arr = np.zeros((101, 101), np.uint8)
    for i in range(101):
        for j in range(101):
            Arr[i, j] += 255
    cv2.imwrite(SavePath + "\\bkimg.png", Arr)
    bkimg = cv2.imread(SavePath + "\\bkimg.png")
    font = ImageFont.truetype(fontpath, 11)
    imgpil = Image.fromarray(bkimg)
    draw = ImageDraw.Draw(imgpil)
    draw.text(
        (0, 0),
        add1
        + "\n"
        + add2
        + "\n"
        + add3
        + "\n"
        + hash1
        + "\n"
        + hash2
        + "\n"
        + hash3
        + "\n",
        font=font,
        fill=(0, 0, 0),
    )
    bkimg = np.array(imgpil)
    cv2.imwrite(SavePath + "\\water.png", bkimg)
    Arnold_img = Arnold(cv2.imread(SavePath + "\\water.png", 0), key, a, b)
    cv2.imwrite(SavePath + "\\watermark.png", Arnold_img)


def buyer_get_J(imgpath, SavePath, name):
    """
    Args:
        imgpath (the image path):

    Returns:
        list: the position of pixel which is bigger than average-pixel
    """
    img = cv2.imread(imgpath, 0)
    lis = []
    r, c = img.shape[0], img.shape[1]
    k = 0
    ave = cv2.meanStdDev(img)[0][0, 0]
    for i in range(r):
        for j in range(c):
            if img[i, j] <= ave:
                lis.append(k)
            k += 1
    with open(SavePath + "\\{}.txt".format(name), "w") as f:
        f.write(str(lis))
    print("write {0} to ".format(name) + SavePath + "\\{0}.txt".format(name))


def envec_dump_json(pubkey, enc_vals, indent=None):
    """Serializes a vector of encrypted numbers into a simple JSON format."""
    from phe.util import int_to_base64

    R = {}
    R["public_key"] = {
        "n": int_to_base64(pubkey.n),
    }
    R["values"] = [(int_to_base64(x.ciphertext()), x.exponent)
                   for x in enc_vals]
    return json.dumps(R, indent=indent)


def envec_load_json(R_json):
    """Deserializes a vector of encrypted numbers."""
    from phe.util import base64_to_int

    R = json.loads(R_json)
    R_pubkey = R["public_key"]
    R_values = R["values"]

    # deserialized values:
    pubkey_d = paillier.PaillierPublicKey(n=base64_to_int(R_pubkey["n"]))
    values_d = [
        paillier.EncryptedNumber(
            pubkey_d, ciphertext=base64_to_int(v[0]), exponent=int(v[1])
        )
        for v in R_values
    ]
    return pubkey_d, values_d


def buyer_save_encryption(cal, ch1, cv1, cd1, pubkey, FileSavePath):
    """
    input: four numpy.ndarray after dwt,public key ,the path to save encrypted data
    output: a list of encrypted data
    """
    lis = []
    lis1 = []
    lis2 = []
    lis3 = []
    lis4 = []
    for i in range(cal.shape[0]):
        for j in range(cal.shape[1]):
            lis1.append(cal[i, j])
            lis2.append(ch1[i, j])
            lis3.append(cv1[i, j])
            lis4.append(cd1[i, j])
    lis = lis1 + lis2 + lis3 + lis4
    en_lis = [pubkey.encrypt(x) for x in lis]
    with open(FileSavePath + "\\encrypted.txt", "w") as f:
        f.write(envec_dump_json(pubkey, en_lis))


def seller_save_encryption(cl, cH3, cV3, cD3, pubkey, FileSavePath):
    """
    input: four numpy.ndarray after dwt,public key ,the path to save encrypted data
    output: a list of encrypted data
    """
    lis = []
    lis1 = []
    lis2 = []
    lis3 = []
    lis4 = []
    for i in range(cl.shape[0]):
        for j in range(cl.shape[1]):
            lis1.append(cl[i, j])
            lis2.append(cH3[i, j])
            lis3.append(cV3[i, j])
            lis4.append(cD3[i, j])
    lis = lis1 + lis2 + lis3 + lis4
    en_lis = [pubkey.encrypt(x) for x in lis]
    with open(FileSavePath + "\\encrypted.txt", "w") as f:
        f.write(envec_dump_json(pubkey, en_lis))


def buyer_load_encryption(file, pubkey):
    with open(file, "r+") as f:
        Strjson = f.read()
        pubkey, Values = envec_load_json(Strjson)
        return pubkey, Values


def seller_load_encryption(file, pubkey):
    with open(file, "r+") as f:
        Strjson = f.read()
        pubkey, Values = envec_load_json(Strjson)
        return pubkey, Values
