from nipype import Node, Workflow
from nipype.interfaces import fsl
from nipype.interfaces.fsl import BET
from pathlib import Path
import os
ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent

in_file = os.path.join(ROOT_DIR, 'data', '031768_t1w_deface_stx.nii.gz')
# workflow
skullstrip = Node(fsl.BET(in_file=in_file, mask=True), name="skullstrip")

smooth = Node(fsl.IsotropicSmooth(in_file=in_file, fwhm=4), name="smooth")

mask = Node(fsl.ApplyMask(), name="mask")

wf = Workflow(name="smoothflow", base_dir=os.path.join(ROOT_DIR, 'nipy_pipeline'))

# First the "simple", but more restricted method
wf.connect(skullstrip, "mask_file", mask, "mask_file")
# Now the more complicated method
wf.connect([(smooth, mask, [("out_file", "in_file")])])
wf.run()