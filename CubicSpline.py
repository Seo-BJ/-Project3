import numpy as np

def NCS_H(x):
    n = len(x)
    h = np.zeros(n-1)
    
    for i in range(n-1):
        h[i] = x[i+1] - x[i]
    return h

import numpy as np

def NCS_Z(x, f):
    n = len(x)
    H = NCS_H(x)  # 앞서 정의한 NCS_H 함수 사용
    
    # 'b' 배열 계산
    b = np.zeros(n-2)
    for i in range(n-2):
        b[i] = (f[i+2] - f[i+1]) / H[i+1] - (f[i+1] - f[i]) / H[i]
        b[i] = 6 * b[i]
    
    # 'h' 행렬 계산
    h = np.zeros((n-2, n-2))
    if n == 3:
        h[0, 0] = 2 * (H[0] + H[1])
    elif n > 3:
        h[0, 0] = 2 * (H[0] + H[1])
        h[0, 1] = H[1]
        h[-1, -2] = H[-2]
        h[-1, -1] = 2 * (H[-2] + H[-1])
        for i in range(1, n-3):
            h[i, i-1] = H[i]
            h[i, i] = 2 * (H[i] + H[i+1])
            h[i, i+1] = H[i+1]

    # 'z' 배열 계산
    z = np.linalg.solve(h, b)

    # 최종 'Z' 배열 계산
    Z = np.zeros(n)
    Z[1:-1] = z

    return Z

import numpy as np
import matplotlib.pyplot as plt

def NCS_Spline(t, x, f, j):
    n = len(x)
    N = len(t)
    spline = np.zeros(N)
    H = NCS_H(x)
    Z = NCS_Z(x, f)

    # 스플라인 수식 정의
    def s(t):
        return (Z[j] / (6 * H[j-1]) * (t - x[j-1])**3 +
                Z[j-1] / (6 * H[j-1]) * (x[j] - t)**3 +
                (f[j] / H[j-1] - Z[j] * H[j-1] / 6) * (t - x[j-1]) +
                (f[j-1] / H[j-1] - Z[j-1] * H[j-1] / 6) * (x[j] - t))

    # 각 t에 대한 스플라인 값 계산
    for i in range(N):
        spline[i] = s(t[i])

    return spline

def NCS_Formula(x, f):
    n = len(x)
    spline_points = []

    for i in range(n-1):
        t = np.linspace(x[i], x[i+1], 100)  # 스플라인을 부드럽게 그리기 위한 충분한 포인트
        s = NCS_Spline(t, x, f, i+1)
        spline_points.extend(list(zip(t, s)))

    return spline_points
