import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Dados
# -----------------------------
dados = [
    ["Masculino", 40190.82, 47],
    ["Masculino", 35433.00, 42],
    ["Masculino", 30186.02, 47],
    ["Masculino", 26471.00, 55],
    ["Masculino", 24664.32, 38],
    ["Feminino", 23654.48, 48],
    ["Masculino", 22575.00, 41],
    ["Masculino", 21200.70, 51],
    ["Masculino", 21184.19, 40],
    ["Masculino", 17107.84, 49],
    ["Masculino", 16169.00, 39],
    ["Masculino", 15956.00, 35],
    ["Masculino", 15675.00, 34],
    ["Masculino", 15379.44, 36],
    ["Feminino", 15254.51, 29],
    ["Feminino", 14500.00, 34],
    ["Masculino", 14210.47, 34],
    ["Masculino", 14118.32, 33],
    ["Masculino", 13011.00, 42],
    ["Masculino", 12809.98, 34],
    ["Masculino", 12101.97, 40],
    ["Masculino", 11998.96, 37],
    ["Masculino", 11360.00, 43],
    ["Masculino", 11200.00, 28],
    ["Masculino", 10764.26, 31],
    ["Masculino", 10733.00, 40],
    ["Masculino", 10326.00, 31],
    ["Masculino", 10191.68, 30],
    ["Feminino", 10022.80, 35],
    ["Masculino", 9984.66, 32],
    ["Masculino", 9808.33, 37],
    ["Masculino", 9292.00, 31],
    ["Masculino", 9197.86, 31],
    ["Masculino", 9047.04, 30],
    ["Masculino", 9000.00, 33],
    ["Masculino", 8726.64, 33],
    ["Masculino", 8389.93, 31],
    ["Masculino", 7965.03, 30],
    ["Feminino", 7890.81, 26],
    ["Masculino", 7627.39, 36],
    ["Feminino", 7559.64, 26],
    ["Masculino", 7509.48, 38],
    ["Masculino", 7371.00, 38],
    ["Masculino", 7331.75, 31],
    ["Masculino", 7208.73, 28],
    ["Masculino", 7011.65, 28],
    ["Feminino", 7000.00, 42],
    ["Feminino", 6705.79, 24],
    ["Masculino", 6485.66, 39],
    ["Masculino", 6447.00, 27],
    ["Masculino", 6046.20, 24],
    ["Masculino", 6045.60, 30],
    ["Masculino", 5934.00, 36],
    ["Masculino", 5814.00, 26],
    ["Masculino", 5671.27, 34],
    ["Feminino", 4750.00, 27],
    ["Masculino", 4538.25, 25],
    ["Feminino", 4434.58, 42],
    ["Feminino", 4000.00, 26],
    ["Feminino", 3695.36, 29],
    ["Masculino", 3010.73, 24],
    ["Masculino", 2500.00, 24],
    ["Masculino", 2500.00, 24],
    ["Masculino", 2267.20, 25],
    ["Feminino", 1902.00, 25],
    ["Masculino", 1800.00, 21],
    ["Masculino", 1445.00, 25],
]

df = pd.DataFrame(dados, columns=["Sexo", "Salario", "Idade"])

# -----------------------------
# Agrupar por idade e sexo (média dos salários)
# -----------------------------
df_media = df.groupby(["Idade", "Sexo"])["Salario"].mean().reset_index()

# -----------------------------
# Plotagem
# -----------------------------
plt.figure(figsize=(10, 6))

for sexo in df_media["Sexo"].unique():
    subset = df_media[df_media["Sexo"] == sexo]
    plt.plot(subset["Idade"], subset["Salario"], marker="o", label=sexo)

plt.title("Variação do Salário conforme a Idade (por Sexo)", fontsize=14)
plt.xlabel("Idade (anos)")
plt.ylabel("Salário médio (R$)")
plt.legend(title="Sexo")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

