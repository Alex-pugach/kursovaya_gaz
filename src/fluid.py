import pandas as pd
from src.interpolator import LinearInterpolator


class Fluid:
    """
    Класс для расчёта свойств газа (PVT-модель)
    """

    def __init__(self, T=310.0):
        # === Данные из моего варианта (hw2_data.csv) ===
        self.M = 0.018
        self.rho_c = 0.6799
        self.xa = 0.8324
        self.xy = 0.2123
        self.T = T

        # Загружаем таблицу для расчёта вязкости
        df = pd.read_csv('interp_data.csv')
        self.xs = df['P_atm'].tolist()
        self.ys = df['mu_cP'].tolist()

        self.mu_interp = LinearInterpolator(self.xs, self.ys)

        # Псевдокритические параметры (примерно)
        self.Pc = 45.0
        self.Tc = 190.0

    def z(self, P):
        """
        Z-фактор.
        Пока считаю по упрощённой формуле, чтобы вся модель работала.
        Позже заменю на нормальный расчёт из hw2.ipynb (GERG-91).
        """
        if P <= 0:
            return 1.0

        Pr = P / self.Pc
        Tr = self.T / self.Tc

        z = 1.0 - 0.15 * Pr / Tr + 0.008 * (Pr / Tr)**2
        return max(0.6, min(z, 1.1))

    def ro(self, P):
        """Плотность газа при пластовых условиях"""
        if P <= 0:
            return 0.0

        Z = self.z(P)
        P_pa = P * 101325
        return (P_pa * self.M) / (Z * 8.314 * self.T)

    def bg(self, P):
        """Объёмный коэффициент газа (B_g)"""
        if P <= 0:
            return 1.0

        Z = self.z(P)
        P_std = 101325.0
        T_std = 293.15
        return (P_std * Z * self.T) / (P * 101325.0 * T_std)

    def mu(self, P):
        """Динамическая вязкость газа"""
        return self.mu_interp.predict(P)
    