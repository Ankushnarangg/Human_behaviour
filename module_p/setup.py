from setuptools import setup, find_packages

setup(
    name="human_behaviour",
    version="1.0.0",
    description="Human-like mouse movement module for Playwright automation",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Ankush Narang",
    author_email="ankushannarang@gmail.com",
    url="https://github.com/yourusername/human_mouse",  # Your project repo or homepage
    packages=find_packages(),
    install_requires=[
        "playwright",
        "numpy",
        # other dependencies 
    ],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
