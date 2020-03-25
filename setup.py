from setuptools import setup, find_packages


def get_requirements():
    with open("requirements.txt", "r") as req:
        requires = req.readlines()
    return [req.strip() for req in requires]


setup(
    name='valejnik_bot',
    version='1.2.0',
    description='Bot for telegram channel',
    url='https://github.com/delatars/valejnik_bot',
    author='Aleksandr Morokov',
    author_email='morocov.ap.muz@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=get_requirements(),
    entry_points={
        'console_scripts': ['valejnik_bot=valejnik_bot.main:main'],
    }
)