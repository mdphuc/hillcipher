from itertools import product
from fractions import Fraction
from root import Root
import itertools
import string
import math
import numpy as np

print("Choose 1 of following options: ")
print("(1) Get key")
print("(2) Encrypt")
print("(3) Decrypt")
print("(4) Continue")
print("(5) Quit")

def test(ciphertext, key, message_combination):
  p = []
  for mc in message_combination:
    # print((''.join(mc), encrypt(''.join(mc), key, 4)))
    if encrypt(''.join(mc), key, 4) == ciphertext:
      p.append(''.join(mc))
  return p


def decrypt(ciphertext, keys, n):
  messages = list(string.ascii_uppercase)
  message_combination = itertools.product(messages, repeat=n)
  plaintext = []
  for key in keys:
    p = test(ciphertext, key, message_combination)
    if len(p) != 0:
      plaintext.append(p)
  if len(plaintext) != 0:
    return plaintext[0]
  else:
    return plaintext


def getkey(plaintext, ciphertext, matrix_size):
  keys = []
  for n in range(matrix_size, matrix_size+1):
    p = plaintext
    c = ciphertext
    plaintext_fragments = list(map(''.join, zip(*[iter(p)]*matrix_size)))


    messageVector = [[0] * (n) for i in range(len(p)//n)]

    cipherMatrix = [[0] * (n) for i in range(len(c)//n)]

    for j in range(len(p)//n):
      for i in range(n*j, n*j + n):
        messageVector[j][i%n] = ord(p[i]) % 65

    for j in range(len(c)//n):
      for i in range(n*j, n*j + n):
        cipherMatrix[j][i%n] = ord(c[i]) % 65

    matrix = []

    count = 0
    for j in range(n):
      m = []
      for i in range(len(p)//n):
        add = messageVector[i] + [cipherMatrix[i][count]]
        m.append(add)
      matrix.append(m)
      count += 1

    mod_root = []

    for i in range(len(matrix)):
      mod_root.append(Root(matrix[i]))

    final_mod_root = list(itertools.product(*mod_root))

    final_final_mod_root = []

    # for fmr in final_mod_root:
    #   fmr_matrix = np.array(fmr)
    #   if int(np.linalg.det(fmr_matrix)) != 0 and int(np.linalg.det(fmr_matrix)) % 2 != 0 and int(np.linalg.det(fmr_matrix)) % 13 != 0:
    #     final_final_mod_root.append(fmr)

    for ffmr in final_mod_root:
      key = ""
      cipher_fragment = ""
      for n in range(matrix_size):
        for m in range(matrix_size):
          key += chr(ffmr[n][m] + 65)
      for pf in plaintext_fragments:
        cipher_fragment += encrypt(pf, key, matrix_size)
      if cipher_fragment == c:      
        keys.append(key)
      
  return keys


def encrypt(plaintext, key, n):
  #Generate key matrix
  keyMatrix = [[0] * n for i in range(n)]

  def getKeyMatrix(key):
    k = 0
    for i in range(n):
        for j in range(n):
            keyMatrix[i][j] = ord(key[k]) % 65
            k += 1

  #Generate message vector
  messageVector = [[0] for i in range(n)]


  for i in range(n):
    messageVector[i][0] = ord(plaintext[i]) % 65

  #Generate cipher message matrix
  cipherMatrix = [[0] for i in range(n)]

  #Convert key into matrix
  getKeyMatrix(key)


  for i in range(n):
    sum_ = 0
    for j in range(n):
      sum_ += messageVector[j][0] * keyMatrix[i][j]
    cipherMatrix[i][0] = sum_ % 26


  #Encrypt using Hill Cipher algorithm
  # for i in range(n):
  #   cipherMatrix[i][0] = 0
  #   for x in range(n):
  #       cipherMatrix[i][0] += (keyMatrix[i][x] *messageVector[x][0])
  #   cipherMatrix[i][0] = cipherMatrix[i][0] % 26


  #Convert calculated number in matrix to string
  CipherText = []
  for i in range(n):
    CipherText.append(chr(cipherMatrix[i][0] + 65))

  return ''.join(CipherText)

      # return plaintext, key

option = input("> ")

while option != "5":
  while option != "1" and option != "2" and option != "3" and option != "4" and option != "5":
    print("Invalid option!")
    option = input("> ")

  if option == "2":
    plaintext = input("Enter plaintext: ").upper()
    n = int(input("Enter n value for nxn matrix: "))

    while n <= 0:
      print("Invalid input!")
      n = int(input("Enter n value for nxn matrix: "))

    while len(plaintext) > n**2:
      print("Length of plaintext should be smaller than or equal to n^2")
      plaintext = input("Enter plaintext: ").upper()
      n = int(input("Enter n value for nxn matrix: "))
    
    key = input("Enter key: ").upper()
    
    while n**2 != len(key):
      print("Invalid key for {0}x{0} matrix".format(n))
      key = input("Enter key: ")

    while len(plaintext) < n**2:
      plaintext += "X"

    cipher = encrypt(plaintext, key, n)
    print(cipher)
  elif option == "1":
    plaintext = input("Enter plaintext: ").upper()
    ciphertext = input("Enter ciphertext: ").upper()
    while len(plaintext) != len(ciphertext):
      print("Length of plaintext should equal to length of ciphertext")
      plaintext = input("Enter plaintext: ").upper()
      ciphertext = input("Enter ciphertext: ").upper()

    while math.sqrt(len(plaintext)).is_integer() == False:
      print("Plaintext should be a perfect square root")
      plaintext = input("Enter plaintext: ").upper()
    keys = getkey(plaintext, ciphertext, int(math.sqrt(len(plaintext))))
    print(keys)
  elif option == "3":
    ciphertext = input("Enter ciphertext: ").upper()
    plaintext = input("Enter plaintext: ").upper()

    while math.sqrt(len(ciphertext)).is_integer() == False:
      print("Ciphertext should be a perfect square root")
      ciphertext = input("Enter ciphertext: ").upper()

    while len(plaintext) != len(ciphertext):
      print("Length of plaintext should equal to length of ciphertext")
      plaintext = input("Enter plaintext: ").upper()
      ciphertext = input("Enter ciphertext: ").upper()

    ciphertext_to_decrypt = input("Enter ciphertext to decrypt: ")

    while math.sqrt(len(ciphertext_to_decrypt)).is_integer() == False:
      print("Ciphertext to decrypt should be a perfect square root")
      ciphertext_to_decrypt = input("Enter ciphertext to decrypt: ").upper()

    keys = getkey(plaintext, ciphertext, int(math.sqrt(len(plaintext))))

    ciphertext_fragments = list(map(''.join, zip(*[iter(ciphertext_to_decrypt)]*int(math.sqrt(len(plaintext))))))

    plaintext_list = []

    for cf in ciphertext_fragments:
      plaintext_list.append(decrypt(cf, keys, int(math.sqrt(len(ciphertext)))))
  

    plaintexts = list(itertools.product(*plaintext_list))

    plt = []

    for plaintext in plaintexts:
      plt.append(''.join(plaintext))
    

    print(keys)
    print(plt)
  
  option = input("> ")

  
# plaintext = "WHYISTHEREPEOPLE"
# ciphertext = "ZXIUUHJRJKWSWFBN"
