from distutils.core import setup

setup(name="FATE",
      version="0.0.1",
      description="Terminal user interface for FATE",
      author="Chiel ten Brinke",
      author_email="ctenbrinke@gmail.com",
      url="http://www.github.com/Chiel92/fate",
      packages=['fatecore',
          'fatecore.undo_system',
          'fatecore.labeling_system',
          'fatecore.filetype_system'
          ],
      scripts=["fate"]
      )
