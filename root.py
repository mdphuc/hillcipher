from fractions import Fraction
import itertools

# matrix = [[22, 7, 24, 8, 25], [18, 19, 7, 4, 20], [17, 4, 15, 4, 9], [14, 15, 11, 4, 22]]

def FinalCheck(matrix, r, n_):
  sum = 0
  for i in range(len(r)):
    sum += r[i]*matrix[n_][i]
  sum -= matrix[n_][len(r)]
  if sum % 26 == 0:
    return True
  else:
    return False

def Root(matrix):
  m = len(matrix[0]) - 1
  n = len(matrix)

  gaussian_matrix = [[0]* (m + 1) for i in range(n)]  

  for k in range(m-1):
    for j in range(n - 1 , k, -1):
      for i in range(m + 1):
        gaussian_matrix[j][i] = matrix[j][i] * matrix[k][k] - matrix[k][i] * matrix[j][k]
    for j in range(n - 1 , k, -1):
      for i in range(m+1):
        matrix[j][i] = gaussian_matrix[j][i]

  for i in range(m+1):
    gaussian_matrix[0][i] = matrix[0][i]
    
  new_matrix = [[0]*m for i in range(n)]

  for i in range(n-1, -1, -1):
    s = 0
    for j in range(0, m):
      if j < i:
        s += gaussian_matrix[i][j]
      elif j > i:
        s += gaussian_matrix[i][j] * new_matrix[j][j]
    if gaussian_matrix[i][i] != 0:
      new_matrix[i][i] = Fraction((gaussian_matrix[i][m] - s), (gaussian_matrix[i][i]), _normalize=False)
    else:
      new_matrix[i][i] = Fraction(0, 1)

    
  # print(gaussian_matrix)

  yo_mod = []

  for i in range(n):
    root_mod = []
    for j in range(m):
      if float(new_matrix[i][j]) != 0:
        ok = False
        n = 1
        while ok == False:
          for x in range(0, 26):
            if (x * new_matrix[i][j].denominator * n - new_matrix[i][j].numerator * n) % 26 == 0:
              root_mod.append(x)
              ok = True
          n += 1
    yo_mod.append(root_mod)

    root_comb = list(itertools.product(*yo_mod))

    check_root = []

    for r in root_comb:
      check = True
      for n_ in range(n):
        check = FinalCheck(matrix, r, n_)
        if check == False:
          check = False
          break
      if check == True:
        check_root.append(r)


    # for r in root_comb:
    #   if (r[0]*22 + r[1]*7 + r[2]*24 + r[3]*8 - 25) % 26 == 0:
    #     print(m)



  # return yo_mod[::-1]
  return check_root

# # print(Root([[22,1,8],[21,4,13]]))

# print(Root([[22, 7, 24, 8, 25], [18, 19, 7, 4, 20], [17, 4, 15, 4, 9], [14, 15, 11, 4, 22]]))
# print(Root([[2, -2, 0, -6], [1, -1, 1, 1], [0, 3, -2, 5]]))