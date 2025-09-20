from setuptools import setup, find_packages

setup(
    name='saudi-regions-widget-py',
    version='2.0.0',
    author='Manus AI (Original by Younis Dany)',
    author_email='support@manus.im',
    description='A Python library for Saudi Arabia regions, cities, and districts data.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/YounisDany/saudi-regions-widget-py',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',
)

