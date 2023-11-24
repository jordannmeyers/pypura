import setuptools

setuptools.setup(
    name='pypura',
    version='0.0.21',
    author='jordannmeyers',
    author_email='jordannmeyers@icloud.com',
    description='Package for interfacing with custom PuraServer',
    long_description='',
    long_description_content_type="text/markdown",
    url='https://https://github.com/jordannmeyers/pypura',
    project_urls = {
        "Bug Tracker": "https://github.com/jordannmeyers/pypura/issues"
    },
    license='MIT',
    packages=['pypura', 'pypura.sensors'],
    install_requires=['more_itertools', 'requests_toolbelt'],
)
