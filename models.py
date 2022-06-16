from pyscipopt import Model, quicksum


class AcPc:

    def __init__(self, N, Q, K, f, p):
        """
        :param N: number of nodes in the network.
        :param Q: set of origin-destination (OD) pairs.
        :param K: set of candidate sites, which can refuel the set of directional arcs for OD pairs.
        :param f: volume of traffic flow on path q.
        :param p:the number of stations to be located.
        """
        self.N = N
        self.Q = Q
        self.K = K
        self.f = f
        self.p = p

        self.model = Model("AcPc")
        """
        decision (binary) variables: 
        z: 1 if service station is built at node, 0 otherwise.
        y: 1 if the flow on path q belonging to set Q is refueled, 0 otherwise.
        """
        z, y = {}, {}

        # add the decision variables
        for q in range(0, len(Q)):
            y[q] = self.model.addVar(vtype="B", name="y(%s)" % q)
        for i in range(0, N):
            z[i] = self.model.addVar(vtype="B", name="z(%s)" % i)

        # constraints
        for q in range(0, len(Q)):
            try:
                self.model.addCons(quicksum(z[i] for i in range(0, N)) == p, "N. Facilities")

            except KeyError:
                pass

        self.model.addCons(quicksum(z[i] for i in range(0, N)) == p, "N. Facilities")

        self.model.setObjective(
            quicksum(f[q] * y[q] for q in range(0, len(Q))),
            "maximize"
        )

        self.model.data = z, y
