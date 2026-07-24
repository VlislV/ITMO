import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("RGR2_A-15_X1-X4.csv", sep=";")
alpha = 0.05
X1 = df['X1']
X2 = df['X2']
X3 = df['X3']
X4 = df['X4']

#==============================Пункт 4.2

m = len(X1)
n = len(X2)

mean1 = X1.mean()
mean2 = X2.mean()

var1 = X1.var(ddof=1)
var2 = X2.var(ddof=1)

std1 = X1.std(ddof=1)
std2 = X2.std(ddof=1)

pooled_var = ((m - 1) * var1 + (n - 1) * var2) / (m + n - 2)

t_stat = (mean1 - mean2) / np.sqrt(pooled_var * (1/m + 1/n))

df_t = m + n - 2
t_crit = stats.t.ppf(1 - alpha/2, df=df_t)
p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=df_t))

alpha = 0.05

x = np.linspace(-7, 7, 3000)
y = stats.t.pdf(x, df_t)

plt.figure(figsize=(12, 7))
plt.plot(x, y, 'b-', linewidth=2.5, 
         label=f'Распределение Стьюдента (df = {df_t})')

plt.fill_between(x[x <= -t_crit], y[x <= -t_crit], 
                 alpha=0.35, color='red',
                 label=f'Критическая область ($\\alpha$ = {alpha})')
plt.fill_between(x[x >= t_crit], y[x >= t_crit], 
                 alpha=0.35, color='red')

plt.axvline(-t_crit, color='red', linestyle=':', linewidth=1.8)
plt.axvline(t_crit, color='red', linestyle=':', linewidth=1.8)

plt.axvline(t_stat, color='green', linestyle='--', linewidth=2.5,
            label=f'$T_{{\\text{{набл}}}}$ = {t_stat:.4f}')

plt.text(-t_crit - 0.4, max(y) * 0.85, f'−{t_crit:.4f}', 
         color='red', fontsize=11, fontweight='bold')
plt.text(t_crit + 0.15, max(y) * 0.85, f'{t_crit:.4f}', 
         color='red', fontsize=11, fontweight='bold')

plt.xlabel('Значение t-статистики', fontsize=13)
plt.ylabel('Плотность вероятности', fontsize=13)
plt.legend(fontsize=12, loc='upper left')
plt.grid(alpha=0.3, linestyle='--')
plt.tight_layout()
plt.show()


#==============================Пункт 4.3

mu0 = 86.28
mean3 = X3.mean()
std3 = X3.std(ddof=1)
var3 = X3.var(ddof=1)

t_stat_4_3 = np.sqrt(n) * (mean3 - mu0) / std3
df_4_3 = n - 1
p_value_4_3 = 2 * stats.t.sf(abs(t_stat_4_3), df=df_4_3)
t_crit_4_3 = stats.t.ppf(1 - alpha/2, df=df_4_3)

x = np.linspace(-4, 4, 2000)
y = stats.t.pdf(x, df_4_3)

plt.figure(figsize=(12, 7))
plt.plot(x, y, 'b-', linewidth=2.5, 
         label=f'Распределение Стьюдента (df = {df_4_3})')

plt.fill_between(x[x <= -t_crit_4_3], y[x <= -t_crit_4_3], 
                 alpha=0.35, color='red',
                 label=f'Критическая область ($\\alpha$ = 0.05)')
plt.fill_between(x[x >= t_crit_4_3], y[x >= t_crit_4_3], 
                 alpha=0.35, color='red')

plt.axvline(-t_crit_4_3, color='red', linestyle=':', linewidth=1.8)
plt.axvline(t_crit_4_3, color='red', linestyle=':', linewidth=1.8)
plt.axvline(t_stat_4_3, color='green', linestyle='--', linewidth=2.5,
            label=f'$T_{{\\text{{набл}}}}$ = {t_stat_4_3:.4f}')

plt.text(-t_crit_4_3 - 0.3, max(y) * 0.85, f'−{t_crit_4_3:.4f}', 
         color='red', fontsize=11, fontweight='bold')
plt.text(t_crit_4_3 + 0.1, max(y) * 0.85, f'{t_crit_4_3:.4f}', 
         color='red', fontsize=11, fontweight='bold')


plt.xlabel('Значение t-статистики', fontsize=13)
plt.ylabel('Плотность вероятности', fontsize=13)
plt.legend(fontsize=12, loc='upper left')
plt.grid(alpha=0.3, linestyle='--')
plt.tight_layout()
plt.show()

#==============================Пункт 4.3

mwu_result = stats.mannwhitneyu(X1, X2, alternative='two-sided')
u_stat = mwu_result.statistic
p_value_4_4 = mwu_result.pvalue
m, n_mwu = len(X1), len(X2)
mean_u = m * n_mwu / 2
std_u = np.sqrt(m * n_mwu * (m + n_mwu + 1) / 12)
z_stat = (u_stat - mean_u) / std_u
p_value_z = 2 * stats.norm.sf(abs(z_stat))


#==============================Пункт 4.4

lambda_param = 0.079

k_intervals = 7

observed_freq, bin_edges = np.histogram(X4, bins=k_intervals)
bin_edges[0] = 0

expected_prob = np.zeros(k_intervals)
for i in range(k_intervals):
    a, b = bin_edges[i], bin_edges[i+1]
    expected_prob[i] = np.exp(-lambda_param * a) - np.exp(-lambda_param * b)
expected_freq = n * expected_prob

print(f"{'Интервал':<20} {'n_k':<10} {'p_k':<15} {'np_k':<10}")
print("-" * 55)
for i in range(k_intervals):
    print(f"[{bin_edges[i]:.2f}, {bin_edges[i+1]:.2f}){'':<6} "
          f"{observed_freq[i]:<10} {expected_prob[i]:<15.6f} {expected_freq[i]:<10.2f}")
    
obs_merged = []
exp_merged = []
intervals_merged = []
probs_merged = []
temp_obs, temp_exp = 0, 0
start_edge = bin_edges[0]

for i in range(len(observed_freq)):
    temp_obs += observed_freq[i]
    temp_exp += expected_freq[i]

    if temp_exp >= 5 or i == len(observed_freq) - 1:
        if i == len(observed_freq) - 1 and temp_exp < 5 and len(obs_merged) > 0:
            obs_merged[-1] += temp_obs
            exp_merged[-1] += temp_exp
            old_start = float(intervals_merged[-1].split(',')[0].strip('['))
            intervals_merged[-1] = f"[{old_start:.2f}, {bin_edges[i+1]:.2f})"
            probs_merged[-1] += temp_exp / n
        else:
            obs_merged.append(temp_obs)
            exp_merged.append(temp_exp)
            intervals_merged.append(f"[{start_edge:.2f}, {bin_edges[i+1]:.2f})")
            probs_merged.append(temp_exp / n)
        temp_obs, temp_exp = 0, 0
        if i + 1 < len(bin_edges) - 1:
            start_edge = bin_edges[i+1]

if exp_merged[-1] < 5 and len(obs_merged) > 1:
    obs_merged[-2] += obs_merged[-1]
    exp_merged[-2] += exp_merged[-1]
    old_start = float(intervals_merged[-2].split(',')[0].strip('['))
    intervals_merged[-2] = f"[{old_start:.2f}, {bin_edges[-1]:.2f})"
    probs_merged[-2] += probs_merged[-1]
    obs_merged.pop()
    exp_merged.pop()
    intervals_merged.pop()
    probs_merged.pop()

m_merged = len(obs_merged)
df_4_5 = m_merged - 1

chi2_stat = sum((o - e)**2 / e for o, e in zip(obs_merged, exp_merged))
p_value_4_5 = stats.chi2.sf(chi2_stat, df_4_5)
chi2_crit = stats.chi2.ppf(1 - alpha, df_4_5)

print(f"lambda      = {lambda_param}")
print(f"Исходных интервалов: {k_intervals}")
print(f"После объединения: m' = {m_merged}")
print(f"Степени свободы: df = {df_4_5}")
print()
print("Интервалы после объединения:")
print(f"{'Интервал':<20} {'n_k':<10} {'p_k':<12} {'np_k':<10}")
print("-" * 52)
for i in range(m_merged):
    print(f"{intervals_merged[i]:<20} {obs_merged[i]:<10} {probs_merged[i]:<12.6f} {exp_merged[i]:<10.2f}")
print()
print(f"χ²_набл = {chi2_stat:.4f}")
print(f"χ²_крит = {chi2_crit:.4f}")
print(f"p-value = {p_value_4_5:.6f}")