from setuptools import find_packages
from setuptools import setup

package_name = 'rosbag2_tools'

setup(
    name=package_name,
    version='0.2.0',
    packages=find_packages(exclude=['**.test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Marcel Zeilinger',
    author_email='marcel.zeilinger@ait.ac.at',
    maintainer='Markus Hofstaetter',
    maintainer_email='markus.hofstaetter@ait.ac.at',
    description='Python processing and visualization of ROS bags',
    license='Apache 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
