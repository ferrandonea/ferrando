from setuptools import setup, find_packages

setup(
    name="ferrando",
    version="0.1.0",
    package_dir={"": "src"},  # Indica a setuptools que los paquetes están en el directorio 'src'
    packages=find_packages(where="src"),  # Busca todos los paquetes en el directorio 'src'
    author="ferrandonea",
    author_email="tu_email@example.com",
    description="Utilidades autorreferentes",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    install_requires=[
        # Aquí puedes listar las dependencias de tu proyecto
    ],
)
