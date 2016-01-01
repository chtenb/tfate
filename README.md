Text User Interface for FATE
============================
This project provides a simple terminal user interface to the fate editor.

How to install
--------------
First clone the project, including submodules, in a folder of your choice.

```
git clone --recursive https://github.com/Chiel92/tfate
```

To update your clone of tfate to the latest version, run

```
git pull && git submodule update --init --recursive
```

There are several options that enable you to start fate from
commandline with the command `fate`.

###Ubuntu
- Add an alias to your .bashrc, like `alias fate="python3 /path/to/tfate/main.py"`.
- Create a bash script, e.g. name `fate`, which just contains the call `python3 "/path/to/tfate/main.py" "$@"` and make sure its folder is in your PATH.

###Windows
Add a startup script to a folder which is in your PATH.
Let's assume that `C:\bin` is in your path.
To be able to start fate from a DOS-like prompt,
add a file named `fate.bat` to `C:\bin` with contents similar to

```
"C:\Program Files (x86)\Python 3.5\python.exe" "C:\path\to\tfate\main.py" "%*"
```

To be able to start fate from a UNIX-like prompt, such as CYGWIN,
add a file named `fate` to `C:\bin` with contents similar to

```
"C:/Program Files (x86)/Python 3.5/python.exe" "/c/path/to/tfate/main.py" "$@"
```

In the latter case you could of course also decide to define an alias.
