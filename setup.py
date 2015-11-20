from distutils.core import setup

# Glob can't go recursively, so we do it manually
import os
all_files = []
for root, dirnames, filenames in os.walk('.'):
    # Exclude all git related files
    if (root.find('.git') == -1
            and root.find('build') == -1
            and root.find('debug') == -1):
        filenames = [root + '/' + f for f in filenames if f.find('.git') == -1
                     and f.find('.sh') == -1
                     and f.find('.txt') == -1
                     and f.find('.md') == -1
                     and f.find('.pyc') == -1
                     and f.find('.swp') == -1
                     and f.find('.yml') == -1
                     and f != 'setup.py']
        if filenames:
            all_files.append(('tfate/' + root, filenames))

print(all_files)

# for filename in all_files:
    # try:
        # os.remove('/usr/local/'+os.path.basename(filename))
    # except Exception as e:
        # print(e)
        # # print(ycm_data_files)
        # # exit()

# This globally installs the packages fate, tui and unicurses and the start script fate
# Maybe its better to just copy the entire sourcetree as data_files, except for the .git dirs
# Idea 2: make tfate a package and all other stuff package_files
# Then install main script globally, which imports tfate
setup(
    name='tfate',
    version='0.1',
    description='Terminal user interface for fate',
    author='Chiel ten Brinke',
    author_email='ctenbrinke@gmail.com',
    url='http://www.github.com/Chiel92/tfate',
    # packages=[
        # 'fate',
        # 'tui',
        # 'unicurses',
        # 'fate.filetype',
        # 'fate.formatting',
        # 'fate.highlighting',
        # 'fate.errorchecking',
        # #'fate.ycm',
        # 'fate.view',
        # 'fate.test',
    # ],
    # package_dir={
        # 'fate': 'libs/fate/fate',
        # 'unicurses': 'libs/unicurses/unicurses'
    # },
    data_files=all_files,
    scripts=['fate']
)

