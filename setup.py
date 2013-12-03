from distutils.core import setup

setup(name="fate",
      version="0.0.1",
      description="Terminal user interface for fate",
      author="Chiel ten Brinke",
      author_email="ctenbrinke@gmail.com",
      url="http://www.github.com/Chiel92/fate",
      packages=['fatecore',
          'fatecore.undo_system',
          'fatecore.labeling_system',
          'fatecore.clipboard_system',
          'fatecore.filetype_system'
          ],
      scripts=["fate"]
      )
