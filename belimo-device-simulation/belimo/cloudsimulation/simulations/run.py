from belimo.cloudsimulation.simulations.config import setup
from belimo.cloudsimulation.simulations.simulation import Simulation


def main(**kwargs):
    Simulation(**setup(**kwargs)).run()


if __name__ == '__main__':
    print("Running simulation")
    main()
