import cx_Freeze

executables = [cx_Freeze.Executable("Swarm.py")]

cx_Freeze.setup(
    name="Swarm",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["gamePlay.py", "serverGame.py", "clientGame.py"]}},
    executables = executables
    )