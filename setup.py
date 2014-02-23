from distutils.core import setup

setup(name='fate',
      version='0.0.1',
      description='Terminal user interface for fate',
      author='Chiel ten Brinke',
      author_email='ctenbrinke@gmail.com',
      url='http://www.github.com/Chiel92/fate',
      package_dir={'fate': 'lib_fate/fate'},
      packages=[
          'tui',
          'fate',
          'fate.labeling_system',
          'fate.filetype_system'
      ],
      scripts=['fate']
      )
