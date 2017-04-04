from setuptools import setup, find_packages

requires = [
    'flask'
]


setup(
    name='aqua',
    version='0.1',
    description='Aqua',
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='',
    author_email='',
    url='',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires
)