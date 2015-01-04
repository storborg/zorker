from __future__ import print_function

from setuptools import setup, find_packages


setup(name='zorker',
      version='0.1',
      description='A Twitter bot to play text adventure games',
      long_description='',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Topic :: Internet :: WWW/HTTP',
      ],
      keywords='zork infocom text adventure twitter bot',
      url='http://github.com/storborg/zorker',
      author='Scott Torborg',
      author_email='storborg@gmail.com',
      install_requires=[
          'tweepy',
          'pexpect',
      ],
      license='MIT',
      packages=find_packages(),
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False,
      entry_points="""\
      [console_scripts]
      zorker = zorker:main
      """)
