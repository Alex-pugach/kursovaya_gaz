class ResProps:
    """Просто храним свойства пласта"""
    def __init__(self, P, V, T):
        self.P = P
        self.V = V
        self.T = T


class Reservoir:
    """
    Модель пласта.
    Давление падает линейно от накопленной добычи.
    """

    def __init__(self, resprops, fluid):
        self.resprops = resprops
        self.fluid = fluid
        # Начальные запасы газа (примерно)
        self.G_init = resprops.V * 0.6 / 1000000   # млн м³

    def p2(self, q_total, dt=1.0):
        """
        Новое давление после шага добычи
        """
        P = self.resprops.P

        if P <= 5:
            return 5.0

        # Накопленная добыча за шаг (млн м³)
        dG = q_total * dt / 1_000_000

        # Простая линейная модель
        Gp = getattr(self, 'Gp', 0) + dG
        self.Gp = Gp

        # Давление падает пропорционально добыче
        P_new = self.resprops.P * (1 - Gp / self.G_init)

        return max(5.0, P_new)