from setuptools import setup, find_packages

setup(
    name='VKMusic',
    version='0.0.1',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/lycantropos/VKMusic',
    license='GNU GPL',
    author='lycantropos',
    author_email='azatibrakov@gmail.com',
    description="Simple application for VK audio administrating",
    install_requires=[
        'SQLAlchemy==1.1.0', 'click==6.6'
    ],
    dependency_links=[
        'git+https://github.com/lycantropos/VKApp.git#egg=VKApp'
    ]
)
