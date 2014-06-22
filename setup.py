from distutils.core import setup

setup(name='tfate',
      version='0.0.1',
      description='Terminal user interface for fate',
      author='Chiel ten Brinke',
      author_email='ctenbrinke@gmail.com',
      url='http://www.github.com/Chiel92/tfate',
      package_dir={'fate': 'libs/fate'},
      packages=[
          'fate',
          'tui',
          'fate.labeling_system',
          'fate.filetype_system'
          ],
      scripts=['fate']
      )
