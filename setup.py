from setuptools import setup

setup(
    name='skripsi 2020',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'matplotlib==3.3.2',
        'nltk==3.5',
        'scipy==1.5.4',
    ],
    packages=[
        'src',
        'src.clustering',
        'src.gui',
        'src.retrieval',
        'src.gui.frame',
        'src.gui.window',
    ],
)
