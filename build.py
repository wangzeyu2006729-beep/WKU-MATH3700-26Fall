"""Build the self-contained quiz from the supplied text; no dependencies."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
raw = (ROOT / 'source.txt').read_text()
raw = re.sub(r'\n\d+\nMATH 3700: Big Data Computing 100-Question Multiple-Choice Quiz', '', raw)
raw = re.sub(r'^MATH 3700: Big Data Computing 100-Question Multiple-Choice Quiz\n', '', raw, flags=re.M)
raw = re.sub(r'^Part [IVX]+ — .*$', '', raw, flags=re.M)
body, key = raw.split('Answer Key with Brief Explanations')
answers = {int(n): (a, re.sub(r'\s+', ' ', e).strip()) for n, a, e in
           re.findall(r'(\d+)\. \(([A-D])\) (.*?)(?=\n\d+\. \([A-D]\)|\Z)', key, re.S)}
chapters = [
    ('大数据基础', 'Big Data & the 5 V’s', 1, 10),
    ('线性代数', 'Linear Algebra Foundations', 11, 34),
    ('矩阵微积分与特征值', 'Matrix Calculus & Eigenvalues', 35, 44),
    ('概率与统计', 'Probability', 45, 74),
    ('维度灾难', 'Curse of Dimensionality', 75, 83),
    ('距离与度量', 'Distances & Metrics', 84, 91),
    ('梯度下降与 SGD', 'Gradient Descent & SGD', 92, 100),
]

def clean(s):
    s = re.sub(r'\s+', ' ', s).strip()
    for a, b in [('̸=','≠'), ('[︃','['), (']︃',']'), ('︁',''), ('︀',''), ('◦','°'), ('∑︁','∑'), ('∏︁','∏')]:
        s = s.replace(a, b)
    return s

questions = []
for n, block in re.findall(r'Q(\d+)\. (.*?)(?=\nQ\d+\.|\Z)', body, re.S):
    n = int(n)
    chunks = re.split(r'^\([A-D]\) ', block, flags=re.M)
    assert len(chunks) == 5, (n, chunks)
    questions.append(dict(id=n, chapter=next(i for i,c in enumerate(chapters) if c[2]<=n<=c[3]),
                          text=clean(chunks[0]), options=list(map(clean, chunks[1:])),
                          answer=answers[n][0], original=answers[n][1]))

# Restore notation broken by copying from the PDF. [[a,b;c,d]] renders a matrix.
overrides = {
4: ('What is the mathematical implication of Variety?', {1:'Diverse data types must be converted into numerical vectors in ℝᵖ so linear algebra applies'}),
6: (None, {0:'3.6 × 10⁶',1:'12 × 10⁶',2:'36 × 10⁶',3:'360 × 10⁶'}),
8: (None, {0:'Raw data → Cleaning → Transform (X ∈ ℝⁿˣᵖ) → Explore → Model → Interpret'}),
9: (None, {0:'It costs O(p), about 10⁴ operations for p = 10,000',1:'It costs O(p²), about 10⁸ operations for p = 10,000',2:'It costs O(log p), about 13 operations for p = 10,000',3:'It costs O(p³), about 10¹² operations for p = 10,000'}),
11: ('A dataset has 1000 patients (observations) and 20 features. In the course convention X ∈ ℝⁿˣᵖ, what are the shape of X and its number of entries?', {}),
12: (None, {0:'(AB)ᵀ = AᵀBᵀ',1:'(AB)ᵀ = ABᵀ',2:'(AB)ᵀ = BᵀAᵀ',3:'(AB)ᵀ = AᵀB'}),
13: ('If A ∈ ℝ³ˣ⁴ and B ∈ ℝ⁴ˣ², what is the shape of AB?', {}),
14: (None, {1:'(AB)C ≠ A(BC) in general',2:'A(B + C) = AB + AC, but AB ≠ BA in general',3:'(AB)ᵀ = AᵀBᵀ'}),
17: ('What is the trace of A = [[2,7;1,6]]?', {}),
18: (None, {3:'tr(AB) = tr(A⁻¹B)'}),
19: ('What is det [[3,1;2,4]]?', {}),
21: (None, {2:'There exists A⁻¹ with AA⁻¹ = I'}),
22: ('If A is invertible, det(A⁻¹) equals', {3:'det(A)²'}),
23: (None, {0:'[[1,2;2,4]]',1:'[[2,0;0,3]]',2:'[[1,2;3,4]]',3:'I₂'}),
24: ('What is ‖v‖₂ for v = (2, −3, 6)ᵀ?', {}),
25: ('For u = (3, −4, 0)ᵀ, the values (‖u‖₁, ‖u‖₂, ‖u‖∞) are', {}),
26: ('Let u = (1, 2, 2)ᵀ and v = (2, −1, 0)ᵀ. What is the angle between them?', {1:'0°'}),
27: (None, {0:'uᵀv ≥ ‖u‖₂‖v‖₂',1:'|uᵀv| ≤ ‖u‖₂‖v‖₂',2:'‖u + v‖₂ ≥ ‖u‖₂ + ‖v‖₂',3:'|uᵀv| ≥ ‖u‖₂‖v‖₂'}),
30: (None, {0:'QᵀQ = QQᵀ = Iₚ (columns and rows are orthonormal)',1:'Q = Qᵀ'}),
32: ('The Frobenius norm of a matrix is the square root of the sum of squares of all entries. What is it for A = [[1,2;2,4]]?', {}),
33: (None, {0:'[[1,2;3,1]]',1:'[[0,1;−1,0]]',2:'[[1,0;2,1]]',3:'[[1,2;2,5]]'}),
35: ('For a ∈ ℝᵖ, the gradient ∇ₓ(aᵀx) is', {2:'Aᵀa'}),
36: ('The gradient ∇ₓ(xᵀAx) equals', {1:'Aᵀx',2:'(A + Aᵀ)x'}),
37: ('The gradient ∇ₓ‖Ax − b‖₂² equals', {1:'2Aᵀ(Ax − b)',2:'Aᵀ(Ax − b)'}),
38: ('The gradient ∇ₓ(xᵀx) is', {1:'xᵀ'}),
39: ('For L(w) = ‖Xw − y‖₂², why is gradient descent preferred over the closed form w = (XᵀX)⁻¹Xᵀy when p is huge?', {1:'Inverting a p × p matrix costs O(p³), which is infeasible for huge p',3:'XᵀX is always singular'}),
40: ('In ridge regression L = ‖Xw − y‖² + λwᵀw, the gradient of the penalty term λwᵀw is', {3:'2λwᵀw'}),
41: ('A neuron has z = wᵀx + b with output error δ = 0.5. Take w = (1, 1)ᵀ, x = (2, −1)ᵀ, η = 0.1. After the update w ← w − ηδx, what is w?', {}),
42: ('Find the eigenvalues of A = [[2,1;1,2]] using det(A − λI) = 0.', {}),
43: ('If A = PDP⁻¹ with D diagonal, then Aᵏ equals', {0:'PᵏDP⁻ᵏ',1:'Dᵏ',2:'PDᵏP⁻¹',3:'PᵏDᵏP⁻¹'}),
44: ('Maximizing wᵀXᵀXw subject to wᵀw = 1 (the PCA problem) is solved by', {1:'the eigenvectors of XᵀX',2:'the inverse of XᵀX',3:'the gradient 2Xᵀw'}),
45: (None, {2:'Pr(⋃ᵢ Aᵢ) = ∑ᵢ Pr(Aᵢ) for disjoint events'}),
54: ('With 10,000 binary word features and 2 classes, how many conditional probabilities Pr(wordⱼ | class) does Naive Bayes need (instead of roughly 2¹⁰⁰⁰⁰ joint probabilities)?', {2:'2¹⁰⁰⁰⁰'}),
56: ('Laplace smoothing, Pr(word | spam) = (count + α)/(Nₛₚₐₘ + 2α), is used mainly to', {}),
63: (None, {0:'Var[X] = E[X²] − (E[X])²',1:'Var[X] = E[X²] + (E[X])²',2:'Var[X] = (E[X])² − E[X²]'}),
66: ('In Bayes’ rule Pr(M | D) = Pr(D | M)Pr(M)/Pr(D), the term Pr(M) is called the', {}),
70: ('Data D = {1, 3, 12, 5, 9} come from a Gaussian with known σ = 2. The MLE of the mean M minimizes ∑(M − x)². What is it?', {}),
76: ('Each axis of [0, 1]ᵖ is divided into 10 bins. How many cells are there when p = 5?', {1:'10⁵ = 100,000',2:'10¹⁰'}),
77: ('For two random points uniform in [0, 1]ᵖ, the typical distance is about √(p/6). What is it for p = 600?', {}),
78: ('As p → ∞, (maxᵢ,ⱼ ‖xᵢ − xⱼ‖ − minᵢ,ⱼ ‖xᵢ − xⱼ‖) / minᵢ,ⱼ ‖xᵢ − xⱼ‖ → 0. What is the consequence for KNN?', {}),
79: ('A unit cube [0, 1]ᵖ has an inner cube of side 0.9. For p = 10, about what fraction of the volume is inside it?', {}),
80: ('To capture 10% of the volume of [0, 1]¹⁰ with a sub-cube, the side length must be about', {}),
82: ('A standard Gaussian N(0, Iₚ) in high dimension concentrates its mass near a sphere (annulus) of radius', {1:'√p',3:'p²'}),
83: ('The Johnson–Lindenstrauss lemma says that n points can be embedded into ℝᵏ preserving pairwise distances up to 1 ± ϵ with', {1:'k = O(n²)',2:'k = O(log n/ϵ²)'}),
89: (None, {0:'cos θ = 1 although L₂ = √14 ≠ 0: cosine ignores magnitude (scale-invariant)'}),
90: ('The edit distance (insertions and deletions only) between x = abcde and y = acfdeg is', {}),
92: (None, {0:'w⁽ᵗ⁺¹⁾ = w⁽ᵗ⁾ + η∇L(w⁽ᵗ⁾)',1:'w⁽ᵗ⁺¹⁾ = w⁽ᵗ⁾ − η∇L(w⁽ᵗ⁾)',2:'w⁽ᵗ⁺¹⁾ = ηw⁽ᵗ⁾ − ∇L(w⁽ᵗ⁾)',3:'w⁽ᵗ⁺¹⁾ = w⁽ᵗ⁾ − ηL(w⁽ᵗ⁾)'}),
93: ('A dataset has n = 10⁸ samples and d = 10⁴ features. One full-batch GD step costs about', {0:'10⁴ FLOPs',1:'10⁸ FLOPs',2:'10¹² FLOPs',3:'10¹⁶ FLOPs'}),
94: ('With n = 10⁸ and mini-batch size B = 256, about how many mini-batch steps cost the same as one full GD step?', {1:'10⁴',2:'3.9 × 10⁵',3:'10⁸'}),
95: ('Minimize L(w) = (w − 3)² with η = 0.1 starting at w⁽⁰⁾ = 0. What is w⁽¹⁾?', {}),
98: ('A mini-batch of B = 512 samples with d = 10³ features stored as 4-byte floats needs about how much memory?', {}),
}

explanations = '''Veracity 指数据的真实性、准确性和可靠性。记住：Volume 是规模，Velocity 是速度，Variety 是多样性。
数据持续高速到来，体现 Velocity。流式算法只扫描一次，保留小型摘要，适合无法完整存储的数据流。
JSON、XML 和日志通常带有键、标签等组织信息，但不要求固定表结构，因此属于半结构化数据（Semi-structured）。
Variety 表示数据类型多样。把文本、图像等转成 ℝᵖ 中的数值向量，才能使用线性代数和机器学习方法。
RGB 有 3 个通道，因此维度 = 224 × 224 × 3 = 150,528。不要只计算像素位置数。
3000 × 4000 = 12,000,000 个像素，乘 3 个通道得到 36,000,000 = 36 × 10⁶ 个数值。
课程的五个 V 是 Volume、Velocity、Variety、Veracity、Value。Validity 不在这一列表中。
先得到原始数据，再清洗、转为矩阵、探索、建模，最后解释结果。这是本课程采用的流程。
常规稠密矩阵求逆的时间复杂度为 O(p³)。p = 10⁴ 时，量级为 10¹²，促使我们采用迭代方法。
W 是学习得到的卷积滤波器权重，X 是图像块，Y 是特征图；b 为偏置。
数据矩阵的每行是一条观测、每列是一个特征，因此形状为 1000 × 20，共 20,000 个元素。
乘积转置需要逆序：(AB)ᵀ = BᵀAᵀ。记住“转置后交换顺序”。
矩阵乘法中间维度必须相等：(3 × 4)(4 × 2) → 3 × 2。
矩阵乘法满足结合律和分配律，但一般不满足交换律，所以 A(B + C) = AB + AC，AB 不一定等于 BA。
R 中 A %*% B 才是矩阵乘积；A * B 表示逐元素相乘。
NumPy 中 * 是逐元素相乘，@ 是矩阵乘法。
迹是主对角线元素之和：tr(A) = 2 + 6 = 8，与非对角元素无关。
迹满足循环不变性，特别是 tr(AB) = tr(BA)。迹一般不具有乘法性。
二阶行列式为 ad − bc，因此 3 × 4 − 1 × 2 = 10。
行列式具有乘法性：det(AB) = det(A)det(B)。
p × p 方阵可逆等价于满秩、行列式非零。rank(A) < p 恰恰意味着不可逆。
由 AA⁻¹ = I，得 det(A)det(A⁻¹) = 1，所以 det(A⁻¹) = 1/det(A)。
矩阵 A 的第二列是第一列的 2 倍，列线性相关；行列式 1 × 4 − 2 × 2 = 0，所以不可逆。
欧氏范数 ‖v‖₂ = √(2² + (−3)² + 6²) = √49 = 7。
L₁ 范数 = 3 + 4 + 0 = 7；L₂ 范数 = √(9 + 16) = 5；L∞ 范数 = max(3, 4, 0) = 4。
内积 uᵀv = 1 × 2 + 2 × (−1) + 2 × 0 = 0。两向量非零且正交，所以夹角为 90°。
柯西–施瓦茨不等式为 |uᵀv| ≤ ‖u‖₂‖v‖₂，可由内积公式与 |cos θ| ≤ 1 得到。
由右手法则 e₁ × e₂ = e₃，结果是 (0, 0, 1)。
第三列是前两列之和，因此列线性相关，秩最多为 2，小于 3；矩阵是奇异矩阵。
正交矩阵的行和列都是标准正交向量，满足 QᵀQ = QQᵀ = I。它的逆等于转置。
m × n 矩阵的最大秩为 min(m, n)。5 × 3 矩阵满秩时，秩为 3。
Frobenius 范数 = √(1² + 2² + 2² + 4²) = √25 = 5。
对称矩阵满足 A = Aᵀ，即 Aᵢⱼ = Aⱼᵢ。D 中两个非对角元素均为 2。
正交变换保持向量长度和点间距离，可理解为旋转或反射。这是 PCA、SVD 中的重要几何性质。
aᵀx 是关于 x 的线性函数，对各分量求导得到固定向量 a。
一般二次型的梯度为 (A + Aᵀ)x。只有当 A 对称时，才可简化为 2Ax。
对 ‖Ax − b‖₂² 使用链式法则，梯度为 2Aᵀ(Ax − b)。注意不能遗漏 Aᵀ。
xᵀx = ∑xᵢ²，逐分量求导得到 2x。
闭式解涉及 p × p 矩阵求逆，常规代价为 O(p³)；梯度下降可通过矩阵–向量乘积迭代求解。
λ 是常数，∇w(λwᵀw) = 2λw。
ηδ = 0.1 × 0.5 = 0.05。w − 0.05x = (1 − 0.1, 1 + 0.05) = (0.9, 1.05)。
det(A − λI) = (2 − λ)² − 1 = 0，得到 λ = 1 或 3。
对角化后 Aᵏ = PDᵏP⁻¹，因为相邻的 P⁻¹P 抵消。对角矩阵的幂只需对每个对角元素取幂。
Rayleigh 商的最大值由 XᵀX 的最大特征值对应的单位特征向量取得，即第一主成分方向。
任意两个事件的概率不必加起来等于 1。互为补集的事件满足这个等式；其他选项是概率的基本性质。
六种等可能结果中有 3 种属于 A，因此 Pr(A) = 3/6 = 1/2。
按课程表述，百分比描述已有数据；概率模型还支持预测与推理，例如贝叶斯更新、期望和大数定律。
条件概率把样本空间限制在 B 中：Pr(A | B) = Pr(A ∩ B)/Pr(B)，前提是 Pr(B) > 0。
先算 Pr(T = 1) = 0.10 + 0.02 = 0.12，再算 0.10/0.12 ≈ 0.8333，故选 0.83。
独立要求 Pr(C = 1 | T = 1) = Pr(C = 1)。0.833 与 0.15 不同，所以两者不独立。
在所有被标记的交易中，欺诈占比为 0.0004/(0.0004 + 0.0096) = 0.04，即 4%。这是精确率的方向。
在所有欺诈交易中，被标记占比为 0.0004/(0.0004 + 0.0001) = 0.80，即 80%。这是召回率的方向。
朴素贝叶斯假设：给定类别之后，各特征条件独立。它不要求特征无条件独立。
每个类别为每个二元特征保留一个条件概率，因此 2 × 10,000 = 20,000。
条件独立使联合概率可分解为乘积：0.05 × 0.03 × 0.20 = 0.0003。
平滑为未出现的词分配非零概率，避免一个零概率让整封邮件的似然乘积变为零。
log 把乘积变为求和，避免很多很小的概率相乘发生数值下溢；log 单调递增，不改变最大值的位置。
连续型变量在单个点上的概率为 0。fₓ 是概率密度，区间概率由积分计算；密度值可以大于 1。
公平骰子的期望 = (1 + 2 + 3 + 4 + 5 + 6)/6 = 3.5。
期望的线性性不要求独立或不相关；在相应期望存在时，E[X + Y] = E[X] + E[Y]。
用期望的线性性并统一到厘米：100 × 1.755 + 3 = 178.5 cm。
Var[S] = ∑Pr(S = s)(s − 3)² = 0.1 × 4 + 0.1 × 1 + 0.5 × 0 + 0.3 × 1 = 0.8。
方差公式是 Var[X] = E[X²] − (E[X])²。E[X − E[X]] 恒为 0，不能作为方差。
按题目给定的 SE = 0.056%，z = 0.30/0.056 ≈ 5.36，大于 1.96，因此拒绝零差异假设。
按题目给定的 SE，95% 区间为 0.30% ± 1.96 × 0.056% ≈ [0.19%, 0.41%]，不包含 0。
Pr(M) 为先验（prior）；Pr(D | M) 为似然，Pr(M | D) 为后验，Pr(D) 为证据。
三家工厂的未归一化权重为 0.50 × 0.01 = 0.005、0.30 × 0.10 = 0.030、0.20 × 0.02 = 0.004。B 的后验为 0.030/0.039 ≈ 0.77。
真阳性权重为 0.99 × 0.001；假阳性权重为 0.05 × 0.999。后验 = 0.00099/(0.00099 + 0.04995) ≈ 1.94%。低患病率不能忽略。
均匀先验对各模型赋予相同权重，因此最大化后验等价于最大化似然。
已知方差的高斯均值 MLE 是样本均值：(1 + 3 + 12 + 5 + 9)/5 = 6，不是中位数 5。
伯努利点击概率的 MLE 为点击数/曝光数 = 2,500,000/50,000,000 = 0.05。
高斯先验的负对数产生 L₂ 平方惩罚，对应 Ridge；Laplace 先验产生 L₁ 惩罚，对应 Lasso。
按课程采用的常规条件，样本增多后似然主导后验，先验影响减弱，MAP 与 MLE 渐近接近。
Beta–Bernoulli 共轭更新：成功数加 1，失败数加 9，得到 Beta(3, 47)，均值 3/(3 + 47) = 6%。
高维空间变得稀疏，距离和体积出现集中现象，覆盖空间所需的数据量可能指数增长。
每个维度 10 格，p 个维度共有 10ᵖ 格；p = 5 时为 100,000。
典型距离约为 √(p/6) = √(600/6) = √100 = 10。
当最远与最近距离的相对差异趋近 0 时，远近难以区分，KNN 的距离判别能力下降。
体积比例等于边长比例的 p 次方：0.9¹⁰ ≈ 0.349，约 35%。
令边长为 s，则 s¹⁰ = 0.1，故 s = 0.1^(1/10) ≈ 0.794。
内球半径为 0.9，体积比例为 0.9¹⁰⁰。外壳占比 = 1 − 0.9¹⁰⁰ ≈ 0.99997。
标准高斯向量满足 E[‖X‖²] = p，因此范数集中在 √p 附近，而不是原点。
JL 引理的目标维度为 O(log n/ϵ²)，主要取决于点数 n 和允许误差 ϵ，而非原始维度 p。
三角不等式为 d(x, y) ≤ d(x, z) + d(z, y)，不要求对每个 z 都取等号。
坐标差的绝对值为 4、3，故 L₁ = 7，L₂ = √(16 + 9) = 5，L∞ = 4。
坐标差绝对值为 3、4、3，因此 L₁ = 10，L∞ = 4。
交集有 red、blue，共 2 个；并集有 5 个。Jaccard 相似度为 2/5，距离为 1 − 2/5 = 0.6。
x · y = 3，两个范数均为 √6，故 cos θ = 3/6 = 1/2，夹角 θ = 60°。
y = 2x，方向相同，所以 cos θ = 1。但距离 ‖y − x‖₂ = ‖x‖₂ = √14，不为 0。
只允许插入和删除时，距离 = |x| + |y| − 2 × LCS 长度。最长公共子序列为 acde，长度 4，故 5 + 6 − 8 = 3。
逐位比较 10101 与 11110，第 2、4、5 位不同，Hamming 距离为 3。
梯度指向局部上升最快方向；最小化损失时沿负梯度更新：w⁽ᵗ⁺¹⁾ = w⁽ᵗ⁾ − η∇L(w⁽ᵗ⁾)。
一次全批梯度计算约为 O(nd)，即 10⁸ × 10⁴ = 10¹² 量级。
一轮遍历需要约 n/B 次更新：10⁸/256 = 390,625 ≈ 3.9 × 10⁵。
L′(w) = 2(w − 3)，所以 L′(0) = −6；更新得到 0 − 0.1 × (−6) = 0.6。
小批量更新次数为 ⌈150/32⌉ = 5；纯 SGD 每个样本更新一次，每轮更新 150 次。
batch_size = 1 表示每次用一个样本计算梯度，即纯 SGD；每个 epoch 有 n 次更新。
存储量 = 512 × 1000 × 4 = 2,048,000 bytes，约 2 MB。这里采用十进制 MB。
学习率过大可能越过最优点甚至发散；过小会使优化缓慢，浪费迭代次数。
Adam 同时维护梯度的一阶矩与平方梯度的二阶矩，实现动量与逐参数自适应步长。'''.splitlines()
assert len(explanations) == 100, len(explanations)
notes = {
3: '原答案表的解释没有直接说明 JSON/XML。此处补充半结构化数据的定义；正确选项 C 保持不变。',
58: '原题 D 把密度称为 likelihood，措辞较宽泛。严格说 fₓ 是概率密度；把观测固定并视作参数的函数时才称为似然。按原题选 D。',
64: '本题按给定 SE 作答。若用两组各 100,000 的独立二项比例直接估算，SE 约为 0.0805%，与原题给值不同，但显著性结论不变。',
65: '此区间沿用 Q64 题目给定的 SE = 0.056%，不对原题参数作修改。',
88: '原题把 angle 与 cosine distance 混用。选项是角度，所以答案为 60°；若定义 cosine distance = 1 − cos θ，则距离为 0.5。',
90: '粘贴文本中的 “acf deg” 按答案表的字符串长度 6 和 LCS = acde 整理为 “acfdeg”，不把排版空格计入字符。',
}
for q in questions:
    n = q['id']
    if n in overrides:
        text, opts = overrides[n]
        if text: q['text'] = text
        for i, value in opts.items(): q['options'][i] = value
    q['explanation'] = explanations[n-1]
    q['note'] = notes.get(n, '')
    del q['original']
assert [q['id'] for q in questions] == list(range(1,101))
assert len(answers) == 100
for q in questions:
    assert len(q['options']) == 4 and all(q['options']) and q['text']
    assert q['answer'] in 'ABCD'
data = {'chapters':[{'name':c[0], 'english':c[1], 'start':c[2], 'end':c[3]} for c in chapters], 'questions':questions}
(ROOT/'questions.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
template = (ROOT/'template.html').read_text()
(ROOT/'index.html').write_text(template.replace('__QUIZ_DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/')))
print('Built index.html: 100 questions, 400 options, 100 original-key answers and Chinese explanations; 7 chapters.')
