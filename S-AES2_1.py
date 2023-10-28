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

def multiply_x(xfx, a):
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

def polynomial_multiply(a, b):
    result = [0, 0, 0, 0]
    xfx = [0, 0, 0, 0]
    multiply_x(xfx, a)
    x2fx = [0, 0, 0, 0]
    multiply_x(x2fx, xfx)
    x3fx = [0, 0, 0, 0]
    multiply_x(x3fx, x2fx)

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

def XOR8(a, b):
    t = [0] * 8
    for i in range(8):
        t[i] = a[i] ^ b[i]
    return t

def XOR4(a, b):
    t = [0] * 4
    for i in range(4):
        t[i] = a[i] ^ b[i]
    return t

def sbox_substitution(temp):
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

def inverse_sbox_substitution(temp):
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

def left_shift(temp):
    #第一字节的右半部分和第二字节的右半部分进行替换
    for i in range(4, 8):
        t = temp[0][i]
        temp[0][i] = temp[1][i]
        temp[1][i] = t



def g_function(temp, rcon):
    t = list(temp)
    for i in range(4):
        tt = t[i + 4]
        t[i + 4] = t[i]
        t[i] = tt

    sbox_substitution(t)
    return XOR8(t, rcon)

def mix_columns(mingwen):
    si_de2jinzhi = [0, 1, 0, 0]
    m00 = list(mingwen[0][:4])
    m10 = list(mingwen[0][4:])
    m01 = list(mingwen[1][:4])
    m11 = list(mingwen[1][4:])
    n00 = XOR4(m00, polynomial_multiply(si_de2jinzhi, m10))
    n10 = XOR4(polynomial_multiply(si_de2jinzhi, m00), m10)
    n01 = XOR4(m01, polynomial_multiply(si_de2jinzhi, m11))
    n11 = XOR4(polynomial_multiply(si_de2jinzhi, m01), m11)
    for i in range(4):
        mingwen[0][i] = n00[i]
        mingwen[0][i + 4] = n10[i]
        mingwen[1][i] = n01[i]
        mingwen[1][i + 4] = n11[i]

def inverse_mix_columns(mingwen):
    er_de2jinzhi = [0, 0, 1, 0]
    jiu_de2jinzhi=[1,0,0,1]
    m00 = list(mingwen[0][:4])
    m10 = list(mingwen[0][4:])
    m01 = list(mingwen[1][:4])
    m11 = list(mingwen[1][4:])
    n00 = XOR4(polynomial_multiply(jiu_de2jinzhi, m00), polynomial_multiply(er_de2jinzhi, m10))
    n10 = XOR4(polynomial_multiply(er_de2jinzhi, m00), polynomial_multiply(jiu_de2jinzhi, m10))
    n01 = XOR4(polynomial_multiply(jiu_de2jinzhi, m01), polynomial_multiply(er_de2jinzhi, m11))
    n11 = XOR4(polynomial_multiply(er_de2jinzhi, m01), polynomial_multiply(jiu_de2jinzhi, m11))
    for i in range(4):
        mingwen[0][i] = n00[i]
        mingwen[0][i + 4] = n10[i]
        mingwen[1][i] = n01[i]
        mingwen[1][i + 4] = n11[i]



def round_key_addition(mingwen, key):
    for i in range(2):
        for j in range(8):
            mingwen[i][j] ^= key[i][j]

def output(a):
    for i in range(2):
        for j in range(8):
            print(a[i][j], end=' ')
    print()


def aes_encrypt(plaintext,key):

    mingwen = [[int(plaintext[i]) for i in range(8)], [int(plaintext[i]) for i in range(8, 16)]]
    key = [[int(key[i]) for i in range(8)], [int(key[i]) for i in range(8, 16)]]

    w0=key[0]
    w1=key[1]
    w2=XOR8(w0, g_function(w1, rcon1))
    w3=XOR8(w2, w1)
    w4=XOR8(w2, g_function(w3, rcon2))
    w5=XOR8(w4, w3)
    key1=[w2,w3]
    key2=[w4,w5]

    round_key_addition(mingwen, key)

    sbox_substitution(mingwen[0])
    sbox_substitution(mingwen[1])
    left_shift(mingwen)
    mix_columns(mingwen)
    round_key_addition(mingwen, key1)

    sbox_substitution(mingwen[0])
    sbox_substitution(mingwen[1])
    left_shift(mingwen)
    round_key_addition(mingwen, key2)

    return mingwen

def aes_double_encrypt(plaintext,key_a,key_b):

    mingwen = [[int(plaintext[i]) for i in range(8)], [int(plaintext[i]) for i in range(8, 16)]]
    key = [[int(key_a[i]) for i in range(8)], [int(key_a[i]) for i in range(8, 16)]]

    w0=key[0]
    w1=key[1]
    w2=XOR8(w0, g_function(w1, rcon1))
    w3=XOR8(w2, w1)
    w4=XOR8(w2, g_function(w3, rcon2))
    w5=XOR8(w4, w3)
    key1=[w2,w3]
    key2=[w4,w5]

    round_key_addition(mingwen, key)

    sbox_substitution(mingwen[0])
    sbox_substitution(mingwen[1])
    left_shift(mingwen)
    mix_columns(mingwen)
    round_key_addition(mingwen, key1)

    sbox_substitution(mingwen[0])
    sbox_substitution(mingwen[1])
    left_shift(mingwen)
    round_key_addition(mingwen, key2)

    key_double= [[int(key_b[i]) for i in range(8)], [int(key_b[i]) for i in range(8, 16)]]
    w0 = key_double[0]
    w1 = key_double[1]
    w2 = XOR8(w0, g_function(w1, rcon1))
    w3 = XOR8(w2, w1)
    w4 = XOR8(w2, g_function(w3, rcon2))
    w5 = XOR8(w4, w3)
    key_double1 = [w2, w3]
    key_double2 = [w4, w5]

    round_key_addition(mingwen, key_double)

    sbox_substitution(mingwen[0])
    sbox_substitution(mingwen[1])
    left_shift(mingwen)
    mix_columns(mingwen)
    round_key_addition(mingwen, key_double1)

    sbox_substitution(mingwen[0])
    sbox_substitution(mingwen[1])
    left_shift(mingwen)
    round_key_addition(mingwen, key_double2)
    return mingwen

def aes_decrypt(ciphertext,key):
    miwen = [[int(ciphertext[i]) for i in range(8)], [int(ciphertext[i]) for i in range(8, 16)]]
    key = [[int(key[i]) for i in range(8)], [int(key[i]) for i in range(8, 16)]]
    w0 = key[0]
    w1 = key[1]
    w2 = XOR8(w0, g_function(w1, rcon1))
    w3 = XOR8(w2, w1)
    w4 = XOR8(w2, g_function(w3, rcon2))
    w5 = XOR8(w4, w3)
    key1 = [w2, w3]
    key2 = [w4, w5]

    # 解密的第一步是逆轮密钥加
    round_key_addition(miwen, key2)
    # 逆行移位

    left_shift(miwen)
    # 逆半字节替代
    inverse_sbox_substitution(miwen[0])
    inverse_sbox_substitution(miwen[1])

    # 逆轮密钥加
    round_key_addition(miwen, key1)
    # 逆列混淆

    inverse_mix_columns(miwen)
     # 逆行移位
    # for _ in range(2):
    left_shift(miwen)
    # 逆半字节替代
    inverse_sbox_substitution(miwen[0])
    inverse_sbox_substitution(miwen[1])

    # 逆轮密钥加
    round_key_addition(miwen, key)

    return miwen


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
    # plaintext = input("请输入16位明文（以0和1表示）: ")
    # key_1 = input("请输入16位密钥（以0和1表示）: ")
    # if len(plaintext) != 16 or len(key_1) != 16:
    #     print("输入长度不正确，请输入16位的明文和密钥。")
    #     return
    # out=aes_encrypt(plaintext,key_1)
    # print out

    ciphertext = input("请输入16位密文（以0和1表示）: ")
    key_2 = input("请输入16位密钥（以0和1表示）: ")
    if len(ciphertext) != 16 or len(key_2) != 16:
        print("输入长度不正确，请输入16位的密文和密钥。")
        return
    aes_decrypt(ciphertext,key_2)

def doublemain():
    # plaintext = input("请输入16位明文（以0和1表示）: ")
    # key_1 = input("请输入16位密钥（以0和1表示）: ")
    # key_2 = input("请输入16位密钥（以0和1表示）: ")
    # if len(plaintext) != 16 or len(key_1) != 16 or  len(key_2) != 16:
    #     print("输入长度不正确，请输入16位的明文和密钥。")
    #     return
    # print("0100101001110100")
    # aes_double_encrypt(plaintext,key_1,key_2)
    # 安装 tqdm 库（如果尚未安装）
    # pip install tqdm

    from tqdm import tqdm

    plaintext = '0110111101101011'
    matching_key_pairs = []

    # 使用 tqdm 创建进度条
    for i in tqdm(range(65536)):
        key_1 = format(i, '016b')  # 将整数转换为16位的二进制字符串
        key_1 = list(map(int, key_1))

        for j in range(65536):
            key_2 = format(j, '016b')  # 将整数转换为16位的二进制字符串
            key_2 = list(map(int, key_2))

            middle_text_1 = aes_encrypt(plaintext, key_1)
            middle_text_2 = aes_decrypt("0100101001110100", key_2)

            if middle_text_1 == middle_text_2:
                matching_key_pairs.append((key_1, key_2))

    # 打印所有匹配的密钥对
    for key_pair in matching_key_pairs:
        print("匹配的密钥1:", key_pair[0])
        print("匹配的密钥2:", key_pair[1])

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

# CBC
def generate_random_IV():
    # 使用Python的随机库生成16位IV
    import random
    return [random.randint(0, 1) for _ in range(16)]

def xor(bit_seq1, bit_seq2):
    return [b1 ^ b2 for b1, b2 in zip(bit_seq1, bit_seq2)]


def CBC_encrypt(plaintext, key):
    # 分割32位明文为两个16位块
    p1 = plaintext[:16]
    p2 = plaintext[16:]
    # 生成随机IV
    IV = generate_random_IV()

    p1 = xor(IV, p1)
    p1 = aes_encrypt(p1, key)
    p1 = [item for sublist in p1 for item in sublist]
    previous = p1
    p2 = xor(previous, p2)
    p2 = aes_encrypt(p2, key)
    p2 = [item for sublist in p2 for item in sublist]
    return IV, p1+p2



def CBC_decrypt(ciphertext, key, IV):
    # 分割32位明文为两个16位块
    c1 = ciphertext[:16]
    c2 = ciphertext[16:]

    previous = c1
    c1 = aes_decrypt(c1,key)
    c1 = [item for sublist in c1 for item in sublist]
    c1 = xor(c1, IV)
    c2 = aes_decrypt(c2,key)
    c2 = [item for sublist in c2 for item in sublist]
    c2 = xor(c2, previous)
    return c1+c2

def test_aes_cbc():
    plain = [1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0]
    key = [0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1]
    iv, cbc_en = CBC_encrypt(plain, key)
    print("iv = ", iv, "cbc加密后：", cbc_en)
    cbc_de = CBC_decrypt(cbc_en,key,iv)

    if(cbc_de == plain):
        print("ture")
    else:
        print("false")

    cbc_en[0:4] = [0,1,1,1]
    print("篡改加密后的密文", cbc_en)
    cbc_de1 = CBC_decrypt(cbc_en,key,iv)
    if(cbc_de1 == plain):
        print("true")
    else:
        print("篡改后不相等")





if __name__ == "__main__":
   #doublemain()
   test_aes_cbc()