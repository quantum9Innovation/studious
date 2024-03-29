import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='studious',
    version='0.1.0',
    author='quantum9innovation',
    author_email='dev.quantum9innovation@gmail.com',
    description='A time manager for people without time.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/quantum9innovation/studious',
    project_urls={
        'Bug Tracker': 'https://github.com/quantum9innovation/studious/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'studious=studious.__main__:go',
        ],
    },
)
