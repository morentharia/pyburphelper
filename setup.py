from setuptools import setup

setup(name='pyburphelper',
      version='0.1',
      description='pyburphelper',
      url='http://github.com/storborg/funniest',
      author='razdva36',
      author_email='mor.entharia@gmail.com',
      license='MIT',
      packages=['pyburphelper'],
      install_requires=[
          'tailer==0.4.1',
          'httpx',
          'furl',
          'trio'
      ],
      python_requires='>=3.8',
      zip_safe=False)
