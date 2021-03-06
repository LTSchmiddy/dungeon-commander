# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['dungeon-commander.py'],
             pathex=['D:\\Github Repos\\dungeon-commander'],
             binaries=[],
             datas=[
                ('./../data', "./data"),
                ('./../templates', "./templates"),
                ('./../static/libs', "./static/libs"),
                ('./../static/scripts', "./static/scripts"),
                ('./../static/browserify_pack', "./static/browserify_pack"),
                ('./../static/styles/main.css', "./static/styles"),
                ('./../static/styles/child_windows/*.css', "./static/styles"),
                ('./../static/styles/fa5-icons.css', "./static/styles"),
                ('./viewport/call_js_scripts', "./calljs"),
                ('./dungeonsheets/forms', "./dungeonsheets/forms"),
                ('./../venv/Lib/site-packages/cefpython3/locales', "./locales"),
                ('./../venv/Lib/site-packages/cefpython3/swiftshader', "./swiftshader"),
                ('./../venv/Lib/site-packages/cefpython3/subprocess.exe', "."),
                ('./../venv/Lib/site-packages/cefpython3/*.dat', "."),
                ('./../venv/Lib/site-packages/cefpython3/*.bin', "."),
                ('./../venv/Lib/site-packages/cefpython3/*.pak', ".")
             ],
             hiddenimports=['pkg_resources', 'pkg_resources.py2_warn'],
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
          [],
          exclude_binaries=True,
          name='dungeon-commander',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='dungeon-commander')
