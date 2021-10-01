# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

added_files = [
         ( 'main.ui', '.' ),
         ( 'icon/app.png', 'icon/' ),
		 ( 'icon/copypaste.png', 'icon/' ),
		 ( 'icon/erase.png', 'icon/' ),
		 ( 'icon/save2file.png', 'icon/' ),
		 ( 'tool/win/.ExifTool_config', 'tool/win/'),
         ]
		 
a = Analysis(['main.py'],
             pathex=['your_path_to_HeadingCalculator_folder'],
             binaries=[('tool/win/exiftool.exe', 'tool/win/')],
             datas=added_files,
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
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
