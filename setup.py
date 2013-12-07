from distutils.core import setup

setup(name="FATE",
      version="0.0.1",
      description="Terminal user interface for FATE",
      author="Chiel ten Brinke",
      author_email="ctenbrinke@gmail.com",
      url="http://www.github.com/Chiel92/fate",
      packages=[
          'tui',
          'tui.fate',
          'tui.fate.undo_system',
          'tui.fate.labeling_system',
          'tui.fate.filetype_system'
          ],
      scripts=["fate"]
      )
