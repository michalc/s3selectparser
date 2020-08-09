import setuptools


def long_description():
    with open('README.md', 'r') as file:
        return file.read()


setuptools.setup(
    name='s3selectparser',
    version='0.0.0',
    author='Michal Charemza',
    author_email='michal@charemza.name',
    description='S3 Select Parser',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/michalc/s3selectparser',
    py_modules=[
        's3selectparser',
    ],
    python_requires='>=3.7.1',
    install_requires=[
        'pyparsing>=2.4.7',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
       ' Programming Language :: SQL',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
