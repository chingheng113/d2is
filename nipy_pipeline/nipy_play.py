from nipype import Node, Workflow
from nipype.interfaces import fsl
from pathlib import Path
import os
ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent

in_file = os.path.join(ROOT_DIR, 'data','031768_t1w_deface_stx_nii.gz')


skullstrip = Node(fsl.BET(in_file=in_file, mask=True), name="skullstrip")
smooth = Node(fsl.IsotropicSmooth(in_file=in_file, fwhm=4), name="smooth")
mask = Node(fsl.ApplyMask(), name="mask")

wf = Workflow(name="smoothflow", base_dir=os.path.join('..', 'data'))

wf.connect(skullstrip, "mask_file", mask, "mask_file")
wf.connect([(smooth, mask, [("out_file", "in_file")])])