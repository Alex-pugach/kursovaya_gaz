class Well:
    """
    Скважина. Считает дебит по закону Дарси (IPR).
    """

    def __init__(self, fluid, k, h, re, rw, pipe=None, name="well"):
        self.fluid = fluid
        self.k = k
        self.h = h
        self.re = re
        self.rw = rw
        self.pipe = pipe
        self.name = name
        self.beta = 0.00852702

    def C(self, P_res):
        mu = self.fluid.mu(P_res)
        if mu <= 0:
            mu = 0.015
        ln_term = (self.re / self.rw) ** 0.5
        C = self.beta * self.k * self.h / (mu * ln_term)
        return C

    def q(self, P_res, P_bhp):
        if P_bhp >= P_res:
            return 0.0
        C = self.C(P_res)
        return C * (P_res - P_bhp)