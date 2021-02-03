from nipype import Node, Workflow
from nipype.interfaces import fsl
from nipype.interfaces.fsl import BET
from pathlib import Path
import os
ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent

in_file = os.path.join(ROOT_DIR, 'data', '031768_t1w_deface_stx.nii.gz')

skullstrip = BET()
skullstrip.inputs.in_file = in_file
skullstrip.inputs.out_file = os.path.join('..', 'data', '031768_t1w_deface_stx_skullstrip.nii.gz')
skullstrip.inputs.mask = True
print(skullstrip.cmdline)

skullstrip.run()

