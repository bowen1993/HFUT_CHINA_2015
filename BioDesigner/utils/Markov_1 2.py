# -*- coding: cp936 -*-
# ʵ��һ������Ʒ�ģ��

import numpy as np
import os
import django
import sys

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import parts



def markov(data_set):
    """
      ʵ��1������Ʒ�ģ�͵Ĳ���ѵ����
      ����ת�Ƹ��ʾ��󣨶�ά���飩��Ԫ��Ԫ��
      
      data_set������ѵ�������ݼ�����ά�б�
    """
    elements = set()
    for data in data_set:
        tmp = set(data)
        elements |= tmp
    elements = tuple(elements)

    n = len(elements)
    A = np.zeros((n, n))
    count = np.zeros((n, 1))
    # ����״̬ת�Ƹ���
    for data in data_set:
        for i in range(len(data)-1):
            a = elements.index(data[i])
            b = elements.index(data[i+1])
            A[a][b] +=1
            count[a] += 1
    for i in range(n):
        if count[i][0] == 0:
            count[i][0] += 1.0      # ��ֹ������ֳ�0����
    A = A / count
    
    return A, elements


def initial(m, n):
    """
    ��ʼ�����������·������

    :param m: ����
    :param n: ����
    :return: ��ʼ�����dp�����path����
    """
    dp = np.tile(-1.0, (m+1, n))    # (m+1��n)��-1���������δ����
    path = np.tile(-1.0, (m+1, n))  # (m+1��n)��-1������·����β

    for i in range(n):
        dp[m][i] = 1       # ���һ����Ԥ���������������ý���������Ϊdp��ʼ����ֵ
    return dp, path


def print_path(elements, s, path):
    """
    ���Ԥ������

    :param elements: Ԫ��Ԫ��
    :param s: ·����ʼ������
    :param path: �洢·����Ϣ�Ķ�ά����
    :return: None
    """
    for step in path:
        t = int(step[s])
        print elements[t],
        s = t
    print


def predict(m, s, A, elements):
    """
      ʵ�ֶ�����s��Ԥ�⣬ʱ�临�Ӷ�O(n^2*m)

      m����ҪԤ�������
      s���Ѹ����Ĺ۲�����
      A��״̬ת�ƾ���
      elements��Ԫ��Ԫ��
    """
    # ��ʼ��dp�����·������
    n = len(elements)
    dp, path = initial(m, n)
    
    # ���Ƽ���dp����
    for i in range(m-1, 0, -1):          # dp����ĵ�0�е������㣬��Ϊֻ�����һ��
        for j in range(n):
            for k in range(n):
                if dp[i][j] < A[j][k]*dp[i+1][k]:
                    dp[i][j] = A[j][k]*dp[i+1][k]
                    path[i][j] = k

    # �Ե�0�н��м���
    c = elements.index(s)
    for k in range(n):
        if dp[0][c] < A[c][k]*dp[1][k]:
            dp[0][c] = A[c][k]*dp[1][k]
            path[0][c] = k

    if dp[0][c] == 0:
        print u"�޷�����Ԥ�⣡"
        return False
    else:
        print_path(elements, c, path)
        return True

def getDataSet():
    partList = list()
    partInList = parts.objects.all()[:5000]
    for p in partInList:
        subStr = p.deep_u_list
        if not subStr or len(subStr) == 0:
            continue
        if subStr.startswith('_'):
            subStr = subStr[1:]
        if subStr.endswith('_'):
            subStr = subStr[:-1]
        subList = subStr.split('_')
        partList.append(subList)
    return partList

if __name__ == "__main__":
    django.setup()
    data_set = getDataSet()
    A, elements = markov(data_set)
    print 'a get'
    predict(2, '151', A, elements)    
    
