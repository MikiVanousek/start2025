from setuptools import setup, find_namespace_packages

setup(
    # Application name:
    name="belimo-cloudsimulation",
    # Version number:
    version=open("version").read(),
    # Application author details:
    author="Volkher Scholz",
    author_email="volkher.scholz@belimo.ch",
    # Packages
    packages=find_namespace_packages(
        include=['belimo.*'],
        exclude=['docs', 'tests*', 'config']),
    entry_points={
        'console_scripts': [
            'run-simulation=belimo.cloudsimulation.simulations.run:main']},
    # Dependencies
    install_requires=['numpy',
                      'scipy',
                      'pandas',
                      'python-dateutil',
                      'pyyaml'],
    # Details
    url="http://www.belimo.ch",
    # license="LICENSE.txt",
    description="Package for simulation of cloud connected devices",
    long_description=open("README.md").read(),
)
