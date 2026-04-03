import math
import os
import matplotlib.pyplot as plt

OUTPUT_DIR = "output_lab4"
FIGURES_DIR = os.path.join(OUTPUT_DIR, "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)
h = 0.272          
delta_h = 0.001    
v0 = 1.050         
delta_v0 = 0.005   
d = 0.010          
delta_t_inst = 1e-6  


materials = {
    "Алюминий": 2.79,
    "Латунь": 8.5,
    "Сталь": 7.9,
    "Дерево": 0.71,
    "Плексиглас": 1.18,
    "Свинец": 11.34
}

material_order = ["Алюминий", "Латунь", "Сталь", "Дерево", "Плексиглас", "Свинец"]

time_data_ms = {
    "Алюминий": [
        149.679, 150.168, 152.644, 150.115, 149.902, 150.628, 150.852, 150.584, 150.227, 150.502,
        149.977, 150.113, 150.626, 150.205, 150.359, 150.112, 150.124, 151.217, 150.604, 149.930,
        151.423, 151.129, 150.081, 150.518, 150.678, 149.977, 150.569, 150.376, 151.060, 150.294
    ],
    "Латунь": [
        150.104, 149.840, 149.983, 150.354, 149.941, 149.961, 150.183, 150.049, 149.914, 150.106,
        149.920, 150.117, 149.821, 150.409, 149.890, 150.277, 149.836, 149.655, 150.048, 150.099,
        151.118, 150.874, 150.536, 150.615, 150.426, 150.202, 149.907, 150.037, 149.823, 150.776
    ],
    "Сталь": [
        149.275, 149.657, 149.945, 150.128, 150.363, 150.187, 149.895, 149.869, 149.758, 149.968,
        150.331, 149.886, 150.296, 149.761, 149.715, 150.928, 149.986, 150.019, 149.828, 149.904,
        149.368, 149.822, 149.913, 150.148, 149.736, 149.813, 149.947, 149.812, 150.091, 149.834
    ],
    "Дерево": [
        150.694, 150.770, 151.824, 151.097, 151.005, 151.734, 151.320, 150.818, 150.995, 151.199,
        151.194, 150.876, 152.212, 151.662, 151.241, 150.859, 150.969, 151.590, 150.997, 150.917,
        151.406, 151.263, 151.623, 151.285, 150.984, 151.509, 151.279, 150.922, 151.513, 150.959
    ],
    "Плексиглас": [
        150.660, 150.539, 150.370, 150.800, 150.504, 150.509, 150.697, 151.150, 150.446, 150.633,
        150.551, 151.033, 151.848, 151.395, 150.954, 150.696, 150.518, 150.700, 150.649, 150.554,
        150.564, 150.566, 151.222, 150.956, 151.195, 150.891, 151.058, 150.540, 150.955, 150.353
    ],
    "Свинец": [
        149.847, 150.106, 150.138, 149.704, 150.288, 150.257, 150.000, 149.949, 150.190, 149.759,
        150.429, 149.901, 150.169, 150.424, 149.799, 149.842, 149.937, 150.805, 150.590, 150.672,
        150.339, 149.917, 149.951, 150.259, 150.107, 149.851, 149.939, 150.000, 150.971, 149.897
    ]
}


def mean(data):
    return sum(data) / len(data)

def variance(data, ddof=1):
    n = len(data)
    if n <= ddof:
        return 0.0
    m = mean(data)
    return sum((x - m)**2 for x in data) / (n - ddof)

def stdev(data, ddof=1):
    return math.sqrt(variance(data, ddof))

def sem(data):
    return stdev(data, ddof=1) / math.sqrt(len(data))


STUDENT_T = {
    2: 12.706, 3: 4.303, 4: 3.182, 5: 2.776, 6: 2.571,
    7: 2.447, 8: 2.365, 9: 2.306, 10: 2.262, 11: 2.228,
    12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131, 16: 2.120,
    17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086, 21: 2.080,
    22: 2.074, 23: 2.069, 24: 2.064, 25: 2.060, 26: 2.056,
    27: 2.052, 28: 2.048, 29: 2.045, 30: 2.042, 31: 2.040,
    32: 2.037, 33: 2.035, 34: 2.032, 35: 2.030, 36: 2.028,
    37: 2.026, 38: 2.024, 39: 2.023, 40: 2.021, 50: 2.009,
    60: 2.000, 100: 1.984, 120: 1.980, 200: 1.972, 500: 1.965, 1000: 1.962
}
def get_t_crit(n, alpha=0.95):
    if n in STUDENT_T:
        return STUDENT_T[n]
    else:
        return 2.0  


results = {}


def mass(density_gcm3, diameter_m):
    volume = (4/3) * math.pi * (diameter_m/2)**3
    density_kgm3 = density_gcm3 * 1000
    return density_kgm3 * volume

masses = {}
for mat, dens in materials.items():
    masses[mat] = mass(dens, d)

time_stats = {}
for mat in material_order:
    t_ms = time_data_ms[mat]
    t_sec = [x / 1000.0 for x in t_ms]  
    n = len(t_sec)
    mean_t = mean(t_sec)
    s_t = stdev(t_sec, ddof=1)
    se_t = sem(t_sec)
    t_crit = get_t_crit(n)
    delta_t_random = t_crit * se_t
    delta_t_total = math.sqrt(delta_t_random**2 + (delta_t_inst/3)**2)
    time_stats[mat] = {
        'n': n,
        'mean_t': mean_t,
        'std_t': s_t,
        'sem_t': se_t,
        't_crit': t_crit,
        'delta_t_random': delta_t_random,
        'delta_t_total': delta_t_total,
        'data_sec': t_sec
    }


g_results = {}
for mat in material_order:
    t = time_stats[mat]['mean_t']
    dt = time_stats[mat]['delta_t_total']
    g = 2 * (h - v0 * t) / (t**2)
    dg_dh = 2 / (t**2)
    dg_dv0 = -2 / t
    dg_dt = -4 * (h - v0 * t) / (t**3) - 2 * v0 / (t**2)
    delta_g = math.sqrt((dg_dh * delta_h)**2 + (dg_dv0 * delta_v0)**2 + (dg_dt * dt)**2)
    g_results[mat] = {'g': g, 'delta_g': delta_g}

def save_csv(filename, headers, rows):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(','.join(headers) + '\n')
        for row in rows:
            f.write(','.join(str(x) for x in row) + '\n')

headers1 = ['Вещество', 'Плотность, г/см³', 'Диаметр, м', 'Масса, кг']
rows1 = []
for mat in material_order:
    rows1.append([mat, materials[mat], d, masses[mat]])
save_csv(os.path.join(OUTPUT_DIR, 'table1.csv'), headers1, rows1)

with open(os.path.join(OUTPUT_DIR, 'table2.csv'), 'w', encoding='utf-8') as f:
    f.write('Номер измерения,' + ','.join(material_order) + '\n')
    for i in range(30):
        row = [str(i+1)]
        for mat in material_order:
            row.append(str(time_data_ms[mat][i]))
        f.write(','.join(row) + '\n')

headers3 = ['Вещество', 'Среднее t, с', 'Станд. отклонение s, с', 'Станд. ошибка, с', 
            'Коэф. Стьюдента', 'Случ. погр. Δt, с', 'Полная погр. Δt, с']
rows3 = []
for mat in material_order:
    s = time_stats[mat]
    rows3.append([mat, s['mean_t'], s['std_t'], s['sem_t'], s['t_crit'], 
                  s['delta_t_random'], s['delta_t_total']])
save_csv(os.path.join(OUTPUT_DIR, 'table3.csv'), headers3, rows3)

headers4 = ['Вещество', 'g, м/с²']
rows4 = [[mat, g_results[mat]['g']] for mat in material_order]
save_csv(os.path.join(OUTPUT_DIR, 'table4.csv'), headers4, rows4)

headers5 = ['Вещество', 'Δg, м/с²']
rows5 = [[mat, g_results[mat]['delta_g']] for mat in material_order]
save_csv(os.path.join(OUTPUT_DIR, 'table5.csv'), headers5, rows5)

print("Обработка завершена. Результаты сохранены в папку", OUTPUT_DIR)