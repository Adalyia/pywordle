from setuptools import setup

readme = ''
with open('README.md') as f:
    readme = f.read()
    
requirements = [
    'termcolor>=1.1.0',
    'tabulate>=0.8.9'
]

extras_require = {
}

packages = [
    'pywordle'
]

setup(
    name='pywordle',
    author='Adalyia',
    url='https://github.com/Adalyia/aiowowapi',
    version='1.0.0',
    packages=packages,
    license='MIT',
    description='A basic Wordle game object in Python',
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data={'pywordle': ['data/*.txt']},
    install_requires=requirements,
    extras_require=extras_require,
    python_requires='>=3.7.0',
    classifiers=[
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: MIT License',
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    ]
)