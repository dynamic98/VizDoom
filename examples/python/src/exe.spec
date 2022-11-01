# -*- mode: python -*-

block_cipher = None

def add_binaries():
    binaries = [
        (r"C:\Users\sci2019\Anaconda3\envs\VizDoom\Lib\site-packages\vizdoom\libmpg123-0.dll", "vizdoom"),
        (r"C:\Users\sci2019\Anaconda3\envs\VizDoom\Lib\site-packages\vizdoom\libsndfile-1.dll", "vizdoom"),
        (r"C:\Users\sci2019\Anaconda3\envs\VizDoom\Lib\site-packages\vizdoom\vizdoom.exe", "vizdoom"),
    ]
    return binaries

def add_resources():
    resources = [
        (r"C:\Users\sci2019\Anaconda3\envs\VizDoom\Lib\site-packages\vizdoom\scenarios\deathmatch.wad", "vizdoom"),
        (r"C:\Users\sci2019\Anaconda3\envs\VizDoom\Lib\site-packages\vizdoom\vizdoom.pk3", "vizdoom"),
        (r"C:\Users\sci2019\Anaconda3\envs\VizDoom\Lib\site-packages\vizdoom\__init__.py", "vizdoom"),
        (r"C:\Users\sci2019\Anaconda3\envs\VizDoom\Lib\site-packages\vizdoom\scenarios", "vizdoom/scenarios"),
        (r"C:\Users\sci2019\Anaconda3\envs\VizDoom\Lib\site-packages\vizdoom\scenarios\deathmatch.cfg", "."),
        (r"scenarios", "scenarios"),
    ]
    return resources

a = Analysis([r"C:\Users\sci2019\Game_Project\VizDoom\examples\python\spectator.py"],
             pathex=[r"C:\Users\sci2019\Game_Project\VizDoom\examples\python\src"],
             binaries=add_binaries(),
             datas=add_resources(),
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='play_vizdoom',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True
)