import math
from src.state import NodeState


class Pipe:
    """ Считаем, на сколько падает давление в НКТ или шлейфе """

    def __init__(self, L, D, roughness, fluid, vertical_depth=0.0):
        self.L = L                    # длина, м
        self.D = D                    # диаметр, м
        self.roughness = roughness    # шероховатость стенок, м
        self.fluid = fluid
        self.H = vertical_depth       # вертикальная часть трубы, м

    def dp(self, P, q):
        """Считает перепад давления в трубе.
        P — давление на входе (атм)
        q — расход (ст.м³/сут) """
        if q <= 0:
            return NodeState(
                name="pipe",
                P_in=P,
                P_out=P,
                dP=0.0,
                q_std=q
            )

        # Берём свойства газа при среднем давлении
        P_avg = P

        rho = self.fluid.ro(P_avg)
        mu = self.fluid.mu(P_avg) / 1000.0
        Bg = self.fluid.bg(P_avg)

        # Объёмный расход при местных условиях
        q_res = q * Bg

        # Скорость газа в трубе
        area = math.pi * (self.D ** 2) / 4.0
        v = (q_res / 86400.0) / area

        # Число Рейнольдса
        Re = (rho * v * self.D) / mu if mu > 0 else 1e6

        # Коэффициент трения
        if Re < 2300:
            # Ламинар
            lam = 64.0 / Re
        else:
            # Турбулентный поток (простые итерации)
            lam = 0.02
            for i in range(30):
                arg = self.roughness / (3.7 * self.D) + 2.51 / (Re * math.sqrt(lam))
                lam_new = (1.0 / (-2 * math.log10(arg))) ** 2
                if abs(lam_new - lam) < 1e-6:
                    break
                lam = lam_new

        # Перепад от трения + гидростатика
        dp_friction = lam * (self.L / self.D) * (rho * v**2 / 2.0)
        dp_gravity = rho * 9.81 * self.H

        dp_atm = (dp_friction + dp_gravity) / 101325.0
        P_out = P - dp_atm

        return NodeState(
            name="pipe",
            P_in=P,
            P_out=max(1.0, P_out),
            dP=dp_atm,
            q_std=q,
            q_res=q_res,
            v=v,
            rho=rho
        )