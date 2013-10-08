from distutils.core import setup

setup(name="pte",
      version="0.0.1",
      description="Terminal user interface for protexted",
      author="Chiel ten Brinke",
      author_email="ctenbrinke@gmail.com",
      url="http://www.github.com/Chiel92/protexted",
      packages=['protexted',
          'protexted.undo_system',
          'protexted.labeling_system',
          'protexted.clipboard_system',
          'protexted.filetype_system'
          ],
      scripts=["pte"]
      )
