from setuptools import setup

requires = ["networkx>=2.2", "wheel"]


setup(
    name='grina',
    version='0.2',
    description="GRIps Network Analysis module.",
    url='',
    author='tokudo',
    author_email='okudo@nii.ac.jp',
    license='MIT',
    keywords='network',
    packages=['grina'],
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3.8',
    ],
)