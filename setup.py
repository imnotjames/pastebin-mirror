from setuptools import setup

setup(
    name='pastebin-mirror',
    version='1.0.0',
    description='Mirror Pastebin to an SQLite DB',
    url='http://github.com/imnotjames/pastebin-mirror',
    author='James Ward',
    author_email='james@notjam.es',
    license='MIT',
    packages=[
        'pastebin-mirror'
    ],
    install_requires=[
      'requests',
    ],
    zip_safe=False
)