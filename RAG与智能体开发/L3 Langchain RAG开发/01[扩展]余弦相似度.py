import numpy as np

"""
计算两个向量的余弦相似度(衡量方向的相似性,剔除长度的影响)
参数:
    vec_a (np.array):向量A
    vec_b (np.array):向量B
返回:
    float:余弦相似度结果(范围[-1,1],越接近1方向越一致)
公式:
    cos_sim = vec_a * vec_b / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
    cos_sim = (vec_a .vec_b)/ (||vec_a|| x ||vec_b||)
    拆解:
    1.点积:vec_a * vec_b = vec_a[0] x vec_b[0] + vec_a[1] x vec_b[1] + ... + vec_a[n] x vec_b[n]
    2.模长:||vec_a|| = 开根号(vec_a[0]^2 + vec_a[1]^2 + ... + vec_a[n]^2)
    3.模长:||vec_b|| = 开根号(vec_b[0]^2 + vec_b[1]^2 + ... + vec_b[n]^2)

A:[0.5,0.5]
B:[0.7,0.7]
C:[0.7,0.5]
D:[-0.6,-0.5]
"""
def get_dot(vec_a, vec_b):
    """计算2个向量的点积,2个向量同纬度数字乘积之和"""
    if len(vec_a) != len(vec_b):
        raise ValueError("2个向量维度数量必须相同")

    dot_sum = 0
    for a,b in zip(vec_a,vec_b):
        dot_sum += a*b
    return dot_sum

def get_norm(vec):
    """计算单个向量的模长: 对向量的每个数字求平方再求和再开根号"""
    sum_square = 0
    for v in vec:
        sum_square += v**2

    # numpy sqrt函数完成开根号
    result = np.sqrt(sum_square)
    return result

def cosine_similarity(vec_a,vec_b):
    res = get_dot(vec_a, vec_b) / (get_norm(vec_a) * get_norm(vec_b))
#     vec_a = np.array(vec_a)
#     vec_b = np.array(vec_b)
#     if vec_a.shape != vec_b.shape:
#         raise ValueError("2个向量必须维度相同")
    #处理模长为0的情况
    if get_norm(vec_a) == 0 or get_norm(vec_b) == 0:
        return 0.0
    # if np.linalg.norm(vec_a) == 0 or np.linalg.norm(vec_b) == 0:
    #     return 0.0
#     res = np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
    return res

if __name__ == "__main__":
    vec_a = [0.5, 0.5]        # vec_a = np.array(vec_a)   vec_a = [0.5 0.5]
    vec_b =[0.7, 0.7]
    vec_c =[0.7, 0.5]
    vec_d =[-0.6, -0.5]

    print("ab:",cosine_similarity(vec_a,vec_b))
    print("ac:", cosine_similarity(vec_a, vec_c))
    print("ad:", cosine_similarity(vec_a, vec_d))
