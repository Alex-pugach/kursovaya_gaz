class ResProps:
    """ Свойства пласта  """
    def __init__(self, P, V, T):
        self.P = P      # текущее пластовое давление, атм
        self.V = V      # объём пласта, м³
        self.T = T      # температура, К


class Reservoir:
    """ Модель пласта, отвечает за материальный баланс """

    def __init__(self, resprops, fluid):
        self.resprops = resprops
        self.fluid = fluid

    def p2(self, q_total, dt=1.0):
        """ Новое пластовое давление после шага dt (сутки)
        при суммарном дебите q_total (ст.м³/сут) """
        P = self.resprops.P

        if P <= 0 or q_total <= 0:
            return P

        Z = self.fluid.z(P)
        rho_res = self.fluid.ro(P)

        # Плотность при стандартных условиях (примерно)
        rho_std = 101325 * self.fluid.M / (8.314 * 293.15)

        # Формула материального баланса
        dP = (Z * rho_std / rho_res) * (q_total / self.resprops.V) * dt

        P_new = P - dP
        return max(5.0, P_new)   # не даём давлению упасть ниже 5 атм