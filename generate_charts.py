import matplotlib.pyplot as plt
import numpy as np

# Nastavi stil
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# 1. INSERT Performance Comparison
fig, ax = plt.subplots()
databases = ['PostgreSQL', 'MySQL', 'MariaDB']
times = [5.22, 1.29, 0.71]
colors = ['#336699', '#dd8800', '#116644']

bars = ax.bar(databases, times, color=colors, alpha=0.8, edgecolor='black')
ax.set_ylabel('Čas (sekunde)', fontsize=14, fontweight='bold')
ax.set_title('INSERT Performanca - 100.000 zapisov', fontsize=16, fontweight='bold')
ax.set_ylim(0, max(times) * 1.2)

for bar, time in zip(bars, times):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{time}s',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('chart1_insert_performance.png', dpi=300, bbox_inches='tight')
print("✓ Graf 1 shranjen: chart1_insert_performance.png")
plt.close()

# 2. SELECT Performance - Without Indexes
fig, ax = plt.subplots(figsize=(14, 8))
queries = ['Simple\nSELECT', 'COUNT', 'AVG\nAgregacija', 'LIKE\nIskanje', 'Range\nPoizvedba', 'ORDER BY']
postgres = [0.52, 4.91, 15.61, 9.06, 25.02, 16.47]
mysql = [3.23, 6.20, 42.99, 26.80, 32.99, 28.97]
mariadb = [0.64, 9.07, 30.08, 17.31, 27.15, 21.42]

x = np.arange(len(queries))
width = 0.25

bars1 = ax.bar(x - width, postgres, width, label='PostgreSQL', color='#336699', alpha=0.8, edgecolor='black')
bars2 = ax.bar(x, mysql, width, label='MySQL', color='#dd8800', alpha=0.8, edgecolor='black')
bars3 = ax.bar(x + width, mariadb, width, label='MariaDB', color='#116644', alpha=0.8, edgecolor='black')

ax.set_ylabel('Čas (milisekunde)', fontsize=14, fontweight='bold')
ax.set_title('SELECT Performanca - Brez indeksov', fontsize=16, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(queries, fontsize=11)
ax.legend(fontsize=12, loc='upper left')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('chart2_select_no_indexes.png', dpi=300, bbox_inches='tight')
print("✓ Graf 2 shranjen: chart2_select_no_indexes.png")
plt.close()

# 3. Index Optimization Impact - ORDER BY
fig, ax = plt.subplots()
databases = ['PostgreSQL', 'MySQL', 'MariaDB']
before = [16.47, 28.97, 21.42]
after = [0.73, 1.76, 1.61]

x = np.arange(len(databases))
width = 0.35

bars1 = ax.bar(x - width/2, before, width, label='Pred indeksi', color='#cc3333', alpha=0.8, edgecolor='black')
bars2 = ax.bar(x + width/2, after, width, label='Po indeksih', color='#33cc33', alpha=0.8, edgecolor='black')

ax.set_ylabel('Čas (milisekunde)', fontsize=14, fontweight='bold')
ax.set_title('ORDER BY Performanca - Vpliv indeksov', fontsize=16, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(databases, fontsize=12)
ax.legend(fontsize=12)
ax.set_ylim(0, max(before) * 1.2)

plt.tight_layout()
plt.savefig('chart3_index_impact.png', dpi=300, bbox_inches='tight')
print("✓ Graf 3 shranjen: chart3_index_impact.png")
plt.close()

# 4. Fedora vs FreeBSD - INSERT Performance
fig, ax = plt.subplots()
platforms = ['Fedora ', 'FreeBSD ']
insert_times = [10.30, 160.61]
colors = ['#2277bb', '#bb7722']

bars = ax.bar(platforms, insert_times, color=colors, alpha=0.8, edgecolor='black')
ax.set_ylabel('Čas (sekunde)', fontsize=14, fontweight='bold')
ax.set_title('INSERT Performanca: Fedora vs FreeBSD - 100.000 zapisov', fontsize=16, fontweight='bold')
ax.set_ylim(0, max(insert_times) * 1.15)

for bar, time in zip(bars, insert_times):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{time}s',
            ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('chart4_fedora_freebsd_insert.png', dpi=300, bbox_inches='tight')
print("✓ Graf 4 shranjen: chart4_fedora_freebsd_insert.png")
plt.close()

# 5. Fedora vs FreeBSD - SELECT Performance
fig, ax = plt.subplots(figsize=(14, 8))
queries = ['Simple\nSELECT', 'COUNT', 'AVG\nAgregacija', 'LIKE\nIskanje', 'Range\nPoizvedba', 'ORDER BY']
fedora = [2.55, 8.67, 20.39, 10.78, 31.66, 19.43]
freebsd = [5.84, 9.12, 23.29, 18.55, 65.01, 17.27]

x = np.arange(len(queries))
width = 0.35

bars1 = ax.bar(x - width/2, fedora, width, label='Fedora ', color='#2277bb', alpha=0.8, edgecolor='black')
bars2 = ax.bar(x + width/2, freebsd, width, label='FreeBSD ', color='#bb7722', alpha=0.8, edgecolor='black')

ax.set_ylabel('Čas (milisekunde)', fontsize=14, fontweight='bold')
ax.set_title('SELECT Performanca: Fedora vs FreeBSD - Brez indeksov', fontsize=16, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(queries, fontsize=11)
ax.legend(fontsize=12)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('chart5_fedora_freebsd_select.png', dpi=300, bbox_inches='tight')
print("✓ Graf 5 shranjen: chart5_fedora_freebsd_select.png")
plt.close()

# 6. Index Impact - Fedora vs FreeBSD ORDER BY
fig, ax = plt.subplots()
categories = ['Fedora\nPred', 'Fedora\nPo', 'FreeBSD\nPred', 'FreeBSD\nPo']
times = [19.43, 0.45, 17.27, 3.50]
colors = ['#cc3333', '#33cc33', '#cc3333', '#33cc33']

bars = ax.bar(categories, times, color=colors, alpha=0.8, edgecolor='black')
ax.set_ylabel('Čas (milisekunde)', fontsize=14, fontweight='bold')
ax.set_title('ORDER BY Performanca - Vpliv indeksov: Fedora vs FreeBSD', fontsize=16, fontweight='bold')
ax.set_ylim(0, max(times) * 1.3)

for i, (bar, time) in enumerate(zip(bars, times)):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{time}ms',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('chart6_os_index_impact.png', dpi=300, bbox_inches='tight')
print("✓ Graf 6 shranjen: chart6_os_index_impact.png")
plt.close()

# 7. Storage Comparison
fig, ax = plt.subplots()
databases = ['PostgreSQL', 'MySQL', 'MariaDB']
sizes = [18.0, 19.06, 19.06]
colors = ['#336699', '#dd8800', '#116644']

bars = ax.bar(databases, sizes, color=colors, alpha=0.8, edgecolor='black')
ax.set_ylabel('Velikost (MB)', fontsize=14, fontweight='bold')
ax.set_title('Poraba prostora - 100.000 zapisov', fontsize=16, fontweight='bold')
ax.set_ylim(0, max(sizes) * 1.2)

for bar, size in zip(bars, sizes):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{size} MB',
            ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('chart7_storage.png', dpi=300, bbox_inches='tight')
print("✓ Graf 7 shranjen: chart7_storage.png")
plt.close()

print("\n" + "="*60)
print("VSI GRAFI USPEŠNO GENERIRANI!")
print("="*60)
print("\nGenerirane datoteke:")
print("  1. chart1_insert_performance.png")
print("  2. chart2_select_no_indexes.png")
print("  3. chart3_index_impact.png")
print("  4. chart4_fedora_freebsd_insert.png")
print("  5. chart5_fedora_freebsd_select.png")
print("  6. chart6_os_index_impact.png")
print("  7. chart7_storage.png")