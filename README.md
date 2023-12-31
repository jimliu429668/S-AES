# S-AES
simple AES by Python

## 过关测试
### 第1关：基本测试
*根据S-AES算法编写和调试程序，提供GUI解密支持用户交互。输入可以是16bit的数据和16bit的密钥，输出是16bit的密文。*
![image](https://github.com/jimliu429668/S-AES/assets/129664900/dbcb789e-7219-4e67-9115-9069b8ef78f9)  
输入的明文是：1000010110100101  
随机生成的密钥是：0110100111000100  
生成的密文是：0011000100010101   
### 第2关：交叉测试
*考虑到是"算法标准"，所有人在编写程序的时候需要使用相同算法流程和转换单元(替换盒、列混淆矩阵等)，以保证算法和程序在异构的系统或平台上都可以正常运行。
选择其他某组的程序进行测试，选择相同的密钥K，用两组编写的程序分别对明文P进行加密得到相同的密文C。*  
测试的明文是：1001101010110010  
测试的密钥是：0110101110001101  
其他组结果是：1100010010111010  
![image](https://github.com/jimliu429668/S-AES/assets/129664900/a84389b9-8e04-499f-ae12-23f3846f99d8)   
本组结果是：1100010010111010   
![image](https://github.com/jimliu429668/S-AES/assets/129664900/3e84cd42-752e-49df-aa6c-b05c43dd5873)   
两组结果相同，交叉测试成功。   
### 第3关：扩展功能
*考虑到向实用性扩展，加密算法的数据输入可以是ASII编码字符串(分组为2 Bytes)，对应地输出也可以是ACII字符串(很可能是乱码)。*   
![image](https://github.com/jimliu429668/S-AES/assets/129664900/570bd205-c71d-4256-afec-fad91de686c8)  
输入明文“hello”
密钥为：1001010011000011
加密后的密文为：100101010111110000001110001000101111111001000111    
（对明文部分不足16bits的填0处理，再进行后续加密）   

### 第4关：多重加密
#### 双重加密
*将S-AES算法通过双重加密进行扩展，分组长度仍然是16 bits，但密钥长度为32 bits。*   
![image](https://github.com/jimliu429668/S-AES/assets/129664900/79af7bff-05ed-4555-b183-c4d1f3ccdd74)   
输入明文为：1011011100111100   
输入32bits密钥为：10100101101001011111010100011101   
经过双重加密得到密文：0110000111101110    

#### 中间相遇攻击
*假设找到了使用相同密钥的明、密文对(一个或多个)，请尝试使用中间相遇攻击的方法找到正确的密钥Key(K1+K2)。*   
![image](https://github.com/jimliu429668/S-AES/assets/129664900/3ec8f9e1-64c5-4fe9-87aa-4521ffb1e517)   
如图即为可能的密钥，无法完全显示，截取部分内容。   

#### 三重加密
*本组选择使用48bits(K1+K2+K3)的模式进行三重加解密。*   
![image](https://github.com/jimliu429668/S-AES/assets/129664900/e66e1fc4-13c2-45a3-ad1d-6b59d4356749)   
输入明文为：1001001011010101   
48bits(K1+K2+K3)密钥为：111100001010010111100111101001010101101011110101   
经过三重加密生成的密文为：0100101011010100   

### 第5关：工作模式
*基于S-AES算法，使用密码分组链(CBC)模式对较长的明文消息进行加密。注意初始向量(16 bits) 的生成，并需要加解密双方共享。
在CBC模式下进行加密，并尝试对密文分组进行替换或修改，然后进行解密，请对比篡改密文前后的解密结果。*  
![image](https://github.com/jimliu429668/S-AES/assets/129664900/754fafe5-5cf4-48df-9ba6-57039c59545b)   
如图在CBC模式下进行加密，对密文分组进行修改，然后进行解密，解密结果不是原明文。

## 核心代码
### S-Box、逆S-Box和替换矩阵
```
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
```
### Rcon常数
```
rcon1 = [1, 0, 0, 0, 0, 0, 0, 0]
rcon2 = [0, 0, 1, 1, 0, 0, 0, 0]
```
### 对输入的多项式a进行乘x操作，并将结果存储在xfx中
```
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
```
### 在GF(2^4)域上，使用既约多项式x^4 + x + 1，对两个多项式a和b进行乘法操作
```
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
```
### 8位异或和4位异或
```
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
```
### s盒替换和逆s盒替换
```
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
```
### 行移位（同逆行移位）
```
def left_shift(temp):
    #第一字节的右半部分和第二字节的右半部分进行替换
    for i in range(4, 8):
        t = temp[0][i]
        temp[0][i] = temp[1][i]
        temp[1][i] = t
```
### g函数
```
def g_function(temp, rcon):
    t = list(temp)
    for i in range(4):
        tt = t[i + 4]
        t[i + 4] = t[i]
        t[i] = tt

    sbox_substitution(t)
    return XOR8(t, rcon)
```
### 列混淆和逆列混淆
```
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
```
### 轮密钥加
```
def round_key_addition(mingwen, key):
    for i in range(2):
        for j in range(8):
            mingwen[i][j] ^= key[i][j]
```
### 
```
def output(a):
    for i in range(2):
        for j in range(8):
            print(a[i][j], end=' ')
    print()
```
### 二进制加密函数
```
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
```
### 双重加密函数
```
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
```
### 三重加密函数
```
def aes_triple_encrypt(plaintext,key_a,key_b,key_c):

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

    key_triple = [[int(key_c[i]) for i in range(8)], [int(key_c[i]) for i in range(8, 16)]]
    w0 = key_triple[0]
    w1 = key_triple[1]
    w2 = XOR8(w0, g_function(w1, rcon1))
    w3 = XOR8(w2, w1)
    w4 = XOR8(w2, g_function(w3, rcon2))
    w5 = XOR8(w4, w3)
    key_triple1 = [w2, w3]
    key_triple2 = [w4, w5]

    round_key_addition(mingwen, key_triple)

    sbox_substitution(mingwen[0])
    sbox_substitution(mingwen[1])
    left_shift(mingwen)
    mix_columns(mingwen)
    round_key_addition(mingwen, key_triple1)

    sbox_substitution(mingwen[0])
    sbox_substitution(mingwen[1])
    left_shift(mingwen)
    round_key_addition(mingwen, key_triple2)

    return mingwen
```
### 二进制解密函数
```
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
```
### 生成随机密钥
```
def generate_random_key():
    random_numbers = [random.randint(0, 1) for _ in range(16)]
    random_key = ''.join(map(str, random_numbers))  # 将随机数列表转换为字符串
    pyperclip.copy(random_key)  # 将生成的随机数复制到剪贴板
    return random_key
```
### ascii加解密
```
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
    def old_aes_encrypt(plaintext, key):
        mingwen = [[int(plaintext[i]) for i in range(8)], [int(plaintext[i]) for i in range(8, 16)]]
        key = [[int(key[i]) for i in range(8)], [int(key[i]) for i in range(8, 16)]]

        w0 = key[0]
        w1 = key[1]
        w2 = XOR8(w0, g_function(w1, rcon1))
        w3 = XOR8(w2, w1)
        w4 = XOR8(w2, g_function(w3, rcon2))
        w5 = XOR8(w4, w3)
        key1 = [w2, w3]
        key2 = [w4, w5]

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
        print("加密后的密文：")
        output(mingwen)

    plaintext_binary = ascii_to_binary(plaintext)

    # 将二进制明文分组
    plaintext_blocks = split_into_blocks(plaintext_binary)

    for block in plaintext_blocks:
        old_aes_encrypt(block, key)

def ascii_decrypt(ciphertext, key):
    def old_aes_decrypt(ciphertext, key):
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

        round_key_addition(miwen, key2)

        left_shift(miwen)
        inverse_sbox_substitution(miwen[0])
        inverse_sbox_substitution(miwen[1])

        round_key_addition(miwen, key1)

        inverse_mix_columns(miwen)

        left_shift(miwen)

        inverse_sbox_substitution(miwen[0])
        inverse_sbox_substitution(miwen[1])

        round_key_addition(miwen, key)
        print("解密后的明文：")
        output(miwen)
    # 将二进制密文分组
    ciphertext_blocks = split_into_blocks(ciphertext)

    decrypted_blocks = []
    for block in ciphertext_blocks:
        decrypted_blocks.append(old_aes_decrypt(block, key))

    decrypted_binary = ''.join(decrypted_blocks)
    decrypted_text = binary_to_ascii(decrypted_binary)

    print("解密后的明文：", decrypted_text)
```
### 二进制加密实现
```
def main_binary():
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
```
### 双重加密实现  
```
def doublemain():
    plaintext = input("请输入16位明文（以0和1表示）: ")
    key_1 = input("请输入第一个16位密钥（以0和1表示）: ")
    key_2 = input("请输入第二个16位密钥（以0和1表示）: ")
    if len(plaintext) != 16 or len(key_1) != 16 or len(key_2) != 16:
        print("输入长度不正确，请输入16位的密文和密钥。")
        return
    ciphertext = aes_double_encrypt(plaintext, key_1, key_2)
    print("双重加密结果为：", ''.join(map(str, ciphertext[0])) + ''.join(map(str, ciphertext[1])))
```
### 双重加密的有效破解方法
```
def double_break():
    plaintext = '0110111101101011'
    ciphertext='0100101001110100'
    table1=[]
    table2=[]
    for i in range(65535):
        key = format(i, '016b')
        table1.append(aes_encrypt(plaintext, key))
        table2.append(aes_decrypt(ciphertext, key))
    for x in range(65535):
        for y in range(65535):
            if table1[x]==table2[y]:
                print(x,y,"密钥对：",format(x, '016b'),format(y, '016b'))
```
### 三重加密过程
```
def triplemain():
    plaintext = input("请输入16位明文（以0和1表示）: ")
    key_1 = input("请输入第一个16位密钥（以0和1表示）: ")
    key_2 = input("请输入第二个16位密钥（以0和1表示）: ")
    key_3 = input("请输入第三个16位密钥（以0和1表示）: ")
    if len(plaintext) != 16 or len(key_1) != 16  or len(key_2) != 16 or len(key_3) != 16:
        print("输入长度不正确，请输入16位的密文和密钥。")
        return
    ciphertext = aes_triple_encrypt(plaintext,key_1,key_2,key_3)
    print("三重加密结果为：",''.join(map(str, ciphertext[0])) + ''.join(map(str, ciphertext[1])))
```
### ascii加解密实现
```
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
    key = input("请输入16位密钥（以0和1表示）: ")
    if len(key) != 16:
        print("密钥长度不正确，请输入16位的密钥。")
        return
    # 解密ASCII字符串
    ascii_decrypt(ciphertext, key)
```
### CBC加解密实现
```
def generate_random_IV():
    # 使用Python的随机库生成16位IV
    import random
    return [random.randint(0, 1) for _ in range(16)]
def xor(bit_seq1, bit_seq2):
    return [b1 ^ b2 for b1, b2 in zip(bit_seq1, bit_seq2)]

#CBC加密
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
    plain = [1,0,1,0,0,1,0,0,1,1,0,0,1,1,1,0,1,0,0,0,1,0,1,0,1,1,0,1,1,1,0,0]
    key = [1,0,1,0,0,1,0,1,1,1,0,0,1,0,1,1]
    plain_ = int(''.join(map(str, plain)))
    key_ = int(''.join(map(str, key)))
    print("原明文：",plain_)
    print("密钥：", key_)
    iv, cbc_en = CBC_encrypt(plain, key)
    iv_ = int(''.join(map(str, iv)))
    cbc_en_ = int(''.join(map(str, cbc_en)))
    print("iv = ", iv_)
    print("cbc加密后密文：", cbc_en_)
    cbc_de = CBC_decrypt(cbc_en,key,iv)
    cbc_de_ = int(''.join(map(str, cbc_de)))
    print("cbc密文篡改前解密生成的明文：", cbc_de_)
    if(cbc_de == plain):
        print("篡改前相等")
    else:
        print("篡改前不相等")

    cbc_en[0:4] = [0,1,1,1]
    cbc_en_ = int(''.join(map(str, cbc_en)))
    print("替换篡改后的密文:", cbc_en_)
    cbc_de1 = CBC_decrypt(cbc_en,key,iv)
    cbc_de1_ = int(''.join(map(str, cbc_de1)))
    print("替换篡改后密文解密生成的明文:", cbc_de1_)
    if(cbc_de1 == plain):
        print("篡改后相等")
    else:
        print("篡改后不相等")
```
### Tkinter GUI界面部分
```
def GUI_binary():
    def encrypt_text():
        plaintext = input_text.get()
        key = key_entry.get()
        if not validate_binary(key):
            messagebox.showerror("输入错误", "密钥应为16位二进制数")
            return
        key = list(map(int, key))
        if len(key) != 16:
            messagebox.showerror("输入错误", "密钥应为16位二进制数")
            return

        ciphertext = aes_encrypt(plaintext, key)
        ciphertext = ''.join(map(str, ciphertext[0]))+''.join(map(str, ciphertext[1]))
        ciphertext_entry.delete(0, tk.END)
        ciphertext_entry.insert(0, ciphertext)
        messagebox.showinfo("Encryption", "成功使用给定密钥加密明文")

    def decrypt_text():
        ciphertext = input_text.get()
        key = key_entry.get()
        if not validate_binary(key):
            messagebox.showerror("输入错误", "密钥应为16位二进制数")
            return
        key = list(map(int, key))
        if len(key) != 16:
            messagebox.showerror("输入错误", "密钥应为16位二进制数")
            return

        plaintext = aes_decrypt(ciphertext, key)
        plaintext = ''.join(map(str, plaintext[0])) + ''.join(map(str, plaintext[1]))
        plaintext_entry.delete(0, tk.END)
        plaintext_entry.insert(0, plaintext)
        messagebox.showinfo("Decryption", "成功使用给定密钥解密密文")

    def validate_binary(binary_string):
        return all(bit in '01' for bit in binary_string)

    def random_key():
        messagebox.showinfo("随机密钥已复制到剪贴板", generate_random_key())

    # 创建主窗口
    root = tk.Tk()
    root.title("S-AES 加解密GUI")

    # 设置GUI窗口大小
    root.geometry("600x400")

    # 创建标签和文本框用于输入明文/密文和密钥
    encrypt_button = tk.Button(root, text="随机生成密钥", command=random_key)
    encrypt_button.pack()
    input_label = tk.Label(root, text="输入明文或密文（16位二进制数）:")
    input_label.pack()
    input_text = tk.Entry(root)
    input_text.pack()

    key_label = tk.Label(root, text="密钥（16位二进制数）:")
    key_label.pack()
    key_entry = tk.Entry(root)
    key_entry.pack()

    # 创建加密和解密按钮
    encrypt_button = tk.Button(root, text="加密", command=encrypt_text)
    encrypt_button.pack()

    decrypt_button = tk.Button(root, text="解密", command=decrypt_text)
    decrypt_button.pack()


    # 创建文本框用于显示明文和密文
    plaintext_label = tk.Label(root, text="明文:")
    plaintext_label.pack()
    plaintext_entry = tk.Entry(root)
    plaintext_entry.pack()

    ciphertext_label = tk.Label(root, text="密文:")
    ciphertext_label.pack()
    ciphertext_entry = tk.Entry(root)
    ciphertext_entry.pack()

    asciiencrypt_button = tk.Button(root, text="ascii加密", command=main_ascii)
    asciiencrypt_button.pack()

    CBCtest_button = tk.Button(root, text="CBC替换篡改测试", command=test_aes_cbc)
    CBCtest_button.pack()

    doubleAEStest_button = tk.Button(root, text="中间相遇攻击破解双重加密", command=double_break)
    doubleAEStest_button.pack()

    tripleAEStest_button = tk.Button(root, text="三重加密", command=triplemain)
    tripleAEStest_button.pack()

    # 启动主事件循环
    root.mainloop()
```

