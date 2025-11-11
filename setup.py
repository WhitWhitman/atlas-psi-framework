from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="atlas-psi-framework",
    version="1.0.0",
    author="Kenneth E. Whitman Jr.",
    author_email="",  # optional, can add later
    description="A Universal Coherence Metric for Crisis Detection in AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/whitwhitman/atlas-psi-framework",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "scipy>=1.7.0",
        "pyyaml>=6.0",
        "python-dateutil>=2.8.0"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
)
