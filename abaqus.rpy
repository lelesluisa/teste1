# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2020 replay file
# Internal Version: 2019_09_13-14.49.31 163176
# Run by luisa on Fri Nov 22 13:42:08 2024
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(1.11979, 1.1169), width=164.833, 
    height=110.796)
session.viewports['Viewport: 1'].makeCurrent()
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
execfile('C:/BPL/CC_otimizacao/Saint_Script_Part.py', __main__.__dict__)
#: usage: ABQcaeK.exe [-h] --nome_da_simulacao NOME_DA_SIMULACAO --garra_S_T_Y
#:                    GARRA_S_T_Y --garra_I_T_Y GARRA_I_T_Y --garra_S_R_Y
#:                    GARRA_S_R_Y --garra_I_R_Y GARRA_I_R_Y --rosca_S_R_X
#:                    ROSCA_S_R_X --rosca_S_R_Z ROSCA_S_R_Z --rosca_I_R_X
#:                    ROSCA_I_R_X --rosca_I_R_Z ROSCA_I_R_Z --parafuso_T_X
#:                    PARAFUSO_T_X --parafuso_T_Z PARAFUSO_T_Z --parafuso_R_X
#:                    PARAFUSO_R_X --parafuso_R_Z PARAFUSO_R_Z
#: ABQcaeK.exe: error: argument --garra_S_T_Y is required
#* Exit code: 0
#* File "C:/BPL/CC_otimizacao/Saint_Script_Part.py", line 1057, in <module>
#*     args = parser.parse_args(sys.argv[idx:])
#* File 
#* "C:\SIMULIA\EstProducts\2020\win_b64\tools\SMApy\python2.7\lib\argparse.py", 
#* line 1701, in parse_args
#*     args, argv = self.parse_known_args(args, namespace)
#* File 
#* "C:\SIMULIA\EstProducts\2020\win_b64\tools\SMApy\python2.7\lib\argparse.py", 
#* line 1733, in parse_known_args
#*     namespace, args = self._parse_known_args(args, namespace)
#* File 
#* "C:\SIMULIA\EstProducts\2020\win_b64\tools\SMApy\python2.7\lib\argparse.py", 
#* line 1957, in _parse_known_args
#*     self.error(_('argument %s is required') % name)
#* File 
#* "C:\SIMULIA\EstProducts\2020\win_b64\tools\SMApy\python2.7\lib\argparse.py", 
#* line 2374, in error
#*     self.exit(2, _('%s: error: %s\n') % (self.prog, message))
#* File 
#* "C:\SIMULIA\EstProducts\2020\win_b64\tools\SMApy\python2.7\lib\argparse.py", 
#* line 2362, in exit
#*     _sys.exit(status)
