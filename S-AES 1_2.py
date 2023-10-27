import random
import tkinter as tk
from tkinter import messagebox
import time
import pyperclip

# S-Box、逆S-Box和替换矩阵
s_box = [
    [9, 4, 10, 11],
    [13, 1, 8, 5],
    [6, 2, 0, 3],
    [12, 14, 15, 7]
]

inv_s_box = [
    [10, 5, 9, 11],
    [1, 7, 8, 15],
    [6, 0, 2, 3],
    [12, 4, 13, 14]
]

replacement_matrix = [
    [0, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 1, 0, 0],
    [0, 1, 0, 1],
    [0, 1, 1, 0],
    [0, 1, 1, 1],
    [1, 0, 0, 0],
    [1, 0, 0, 1],
    [1, 0, 1, 0],
    [1, 0, 1, 1],
    [1, 1, 0, 0],
    [1, 1, 0, 1],
    [1, 1, 1, 0],
    [1, 1, 1, 1]
]

# Rcon常数
rcon1 = [1, 0, 0, 0, 0, 0, 0, 0]
rcon2 = [0, 0, 1, 1, 0, 0, 0, 0]

def x_de_n_fang_cheng_fx(xfx, a):
    # 注意要取模，既约多项式是x^4 + x + 1
    if a[0] == 0:
        xfx[0] = a[1]
        xfx[1] = a[2]
        xfx[2] = a[3]
        xfx[3] = 0
    else:
        xfx[0] = a[1]
        xfx[1] = a[2]
        xfx[2] = a[3] ^ 1
        xfx[3] = 1

def chengfa(a, b):
    result = [0, 0, 0, 0]
    xfx = [0, 0, 0, 0]
    x_de_n_fang_cheng_fx(xfx, a)
    x2fx = [0, 0, 0, 0]
    x_de_n_fang_cheng_fx(x2fx, xfx)
    x3fx = [0, 0, 0, 0]
    x_de_n_fang_cheng_fx(x3fx, x2fx)

    if b[0] == 1:
        for i in range(4):
            result[i] ^= x3fx[i]
    if b[1] == 1:
        for i in range(4):
            result[i] ^= x2fx[i]
    if b[2] == 1:
        for i in range(4):
            result[i] ^= xfx[i]
    if b[3] == 1:
        for i in range(4):
            result[i] ^= a[i]
    return result

def yihuo8(a, b):
    t = [0] * 8
    for i in range(8):
        t[i] = a[i] ^ b[i]
    return t

def yihuo4(a, b):
    t = [0] * 4
    for i in range(4):
        t[i] = a[i] ^ b[i]
    return t

def s_he_tihuan(temp):
    t1 = 2 * temp[0] + temp[1]
    t2 = 2 * temp[2] + temp[3]
    t3 = 2 * temp[4] + temp[5]
    t4 = 2 * temp[6] + temp[7]

    tihuan1 = s_box[t1][t2]
    tihuan2 = s_box[t3][t4]

    for i in range(4):
        temp[i] = replacement_matrix[tihuan1][i]
    for i in range(4):
        temp[i + 4] = replacement_matrix[tihuan2][i]

def inv_s_he_tihuan(temp):
    t1 = 2 * temp[0] + temp[1]
    t2 = 2 * temp[2] + temp[3]
    t3 = 2 * temp[4] + temp[5]
    t4 = 2 * temp[6] + temp[7]
    tihuan1 = inv_s_box[t1][t2]
    tihuan2 = inv_s_box[t3][t4]

    for i in range(4):
        temp[i] = replacement_matrix[tihuan1][i]
    for i in range(4):
        temp[i + 4] = replacement_matrix[tihuan2][i]

def zuoyi(temp):
    #第一字节的右半部分和第二字节的右半部分进行替换
    for i in range(4, 8):
        t = temp[0][i]
        temp[0][i] = temp[1][i]
        temp[1][i] = t

def g(temp, rcon):
    t = list(temp)
    for i in range(4):
        tt = t[i + 4]
        t[i + 4] = t[i]
        t[i] = tt

    s_he_tihuan(t)
    return yihuo8(t, rcon)

def liehunxiao(mingwen):
    si_de2jinzhi = [0, 1, 0, 0]
    m00 = list(mingwen[0][:4])
    m10 = list(mingwen[0][4:])
    m01 = list(mingwen[1][:4])
    m11 = list(mingwen[1][4:])
    n00 = yihuo4(m00, chengfa(si_de2jinzhi, m10))
    n10 = yihuo4(chengfa(si_de2jinzhi, m00), m10)
    n01 = yihuo4(m01, chengfa(si_de2jinzhi, m11))
    n11 = yihuo4(chengfa(si_de2jinzhi, m01), m11)
    for i in range(4):
        mingwen[0][i] = n00[i]
        mingwen[0][i + 4] = n10[i]
        mingwen[1][i] = n01[i]
        mingwen[1][i + 4] = n11[i]

def inv_liehunxiao(mingwen):
    er_de2jinzhi = [0, 0, 1, 0]
    jiu_de2jinzhi=[1,0,0,1]
    m00 = list(mingwen[0][:4])
    m10 = list(mingwen[0][4:])
    m01 = list(mingwen[1][:4])
    m11 = list(mingwen[1][4:])
    n00 = yihuo4(chengfa(jiu_de2jinzhi,m00), chengfa(er_de2jinzhi, m10))
    n10 = yihuo4(chengfa(er_de2jinzhi, m00), chengfa(jiu_de2jinzhi, m10))
    n01 = yihuo4(chengfa(jiu_de2jinzhi, m01), chengfa(er_de2jinzhi, m11))
    n11 = yihuo4(chengfa(er_de2jinzhi, m01), chengfa(jiu_de2jinzhi, m11))
    for i in range(4):
        mingwen[0][i] = n00[i]
        mingwen[0][i + 4] = n10[i]
        mingwen[1][i] = n01[i]
        mingwen[1][i + 4] = n11[i]



def lunmiyaojia(mingwen, key):
    for i in range(2):
        for j in range(8):
            mingwen[i][j] ^= key[i][j]

def shuchu(a):
    for i in range(2):
        for j in range(8):
            print(a[i][j], end=' ')
    print()


def aes_encrypt(plaintext,key):

    mingwen = [[int(plaintext[i]) for i in range(8)], [int(plaintext[i]) for i in range(8, 16)]]
    key = [[int(key[i]) for i in range(8)], [int(key[i]) for i in range(8, 16)]]

    w0=key[0]
    w1=key[1]
    w2=yihuo8(w0, g(w1, rcon1))
    w3=yihuo8(w2, w1)
    w4=yihuo8(w2, g(w3, rcon2))
    w5=yihuo8(w4,w3)
    key1=[w2,w3]
    key2=[w4,w5]

    lunmiyaojia(mingwen, key)

    s_he_tihuan(mingwen[0])
    s_he_tihuan(mingwen[1])
    zuoyi(mingwen)
    liehunxiao(mingwen)
    lunmiyaojia(mingwen, key1)

    s_he_tihuan(mingwen[0])
    s_he_tihuan(mingwen[1])
    zuoyi(mingwen)
    lunmiyaojia(mingwen, key2)
    print("加密后的密文：（应得出0000 0111 0011 1000）")
    shuchu(mingwen)

def aes_decrypt(ciphertext,key):
    miwen = [[int(ciphertext[i]) for i in range(8)], [int(ciphertext[i]) for i in range(8, 16)]]
    key = [[int(key[i]) for i in range(8)], [int(key[i]) for i in range(8, 16)]]
    w0 = key[0]
    w1 = key[1]
    w2 = yihuo8(w0, g(w1, rcon1))
    w3 = yihuo8(w2, w1)
    w4 = yihuo8(w2, g(w3, rcon2))
    w5 = yihuo8(w4, w3)
    key1 = [w2, w3]
    key2 = [w4, w5]

    # 解密的第一步是逆轮密钥加
    lunmiyaojia(miwen, key2)
    # 逆行移位
    for _ in range(2):
        zuoyi(miwen)
    # 逆半字节替代
    inv_s_he_tihuan(miwen[0])
    inv_s_he_tihuan(miwen[1])

    # 逆轮密钥加
    lunmiyaojia(miwen, key1)
    # 逆列混淆
    for _ in range(2):
        inv_liehunxiao(miwen)
     # 逆行移位
    for _ in range(2):
        zuoyi(miwen)
    # 逆半字节替代
    inv_s_he_tihuan(miwen[0])
    inv_s_he_tihuan(miwen[1])

    # 逆轮密钥加
    lunmiyaojia(miwen, key)
    print("解密后的明文：（应得出0110 1111 0110 1011）")
    shuchu(miwen)


def generate_random_key():
    random_numbers = [random.randint(0, 1) for _ in range(10)]
    random_key = ''.join(map(str, random_numbers))  # 将随机数列表转换为字符串
    pyperclip.copy(random_key)  # 将生成的随机数复制到剪贴板
    return random_key


def ascii_to_binary(ascii_text):
    # 将ASCII编码的文本转换为二进制字符串
    binary_text = ''.join(format(ord(char), '08b') for char in ascii_text)
    return binary_text

def binary_to_ascii(binary_text):
    # 将二进制字符串转换为ASCII编码的文本
    ascii_text = ''.join(chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8))
    return ascii_text

def split_into_blocks(binary_text, block_size=16):
    # 将二进制文本分割成指定大小的块，不足块大小的部分将填充0
    blocks = [binary_text[i:i+block_size] for i in range(0, len(binary_text), block_size)]
    for i in range(len(blocks)):
        if len(blocks[i]) < block_size:
            blocks[i] = blocks[i].ljust(block_size, '0')
    return blocks

def ascii_encrypt(plaintext, key):
    plaintext_binary = ascii_to_binary(plaintext)

    # 将二进制明文分组
    plaintext_blocks = split_into_blocks(plaintext_binary)

    for block in plaintext_blocks:
        aes_encrypt(block, key)

def ascii_decrypt(ciphertext, key):

    # 将二进制密文分组
    ciphertext_blocks = split_into_blocks(ciphertext)

    decrypted_blocks = []
    for block in ciphertext_blocks:
        decrypted_blocks.append(aes_decrypt(block, key))

    decrypted_binary = ''.join(decrypted_blocks)
    decrypted_text = binary_to_ascii(decrypted_binary)

    print("解密后的明文：", decrypted_text)


def main():
    # mingwen = [[0, 1, 1, 0, 1, 1, 1, 1], [0, 1, 1, 0, 1, 0, 1, 1]]  0110111101101011
    # key = [[1, 0, 1, 0, 0, 1, 1, 1], [0, 0, 1, 1, 1, 0, 1, 1]]  1010011100111011
    # miwen = [[0, 0, 0, 0, 0, 1, 1, 1], [0, 0, 1, 1, 1, 0, 0, 0]]  0000011100111000
    # key = [[1, 0, 1, 0, 0, 1, 1, 1], [0, 0, 1, 1, 1, 0, 1, 1]]  1010011100111011
    plaintext = input("请输入16位明文（以0和1表示）: ")
    key = input("请输入16位密钥（以0和1表示）: ")
    if len(plaintext) != 16 or len(key) != 16:
        print("输入长度不正确，请输入16位的明文和密钥。")
        return
    aes_encrypt(plaintext,key)

    ciphertext = input("请输入16位密文（以0和1表示）: ")
    key = input("请输入16位密钥（以0和1表示）: ")
    if len(ciphertext) != 16 or len(key) != 16:
        print("输入长度不正确，请输入16位的密文和密钥。")
        return
    aes_decrypt()

def main_ascii():
    plaintext = input("请输入ASCII编码的明文: ")
    key = input("请输入16位密钥（以0和1表示）: ")

    if len(key) != 16:
        print("密钥长度不正确，请输入16位的密钥。")
        return

    # 加密ASCII字符串
    ascii_encrypt(plaintext, key)

    ciphertext = input("请输入16位ASCII编码的密文: ")

    if len(ciphertext) != 16:
        print("密文长度不正确，请输入16位的密文。")
        return

    # 解密ASCII字符串
    ascii_decrypt(ciphertext, key)

if __name__ == "__main__":
    main_ascii()
