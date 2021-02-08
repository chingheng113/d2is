from nipype import Node, Workflow
from nipype.interfaces import fsl
from nipype.interfaces.fsl import BET
from pathlib import Path
import os
ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent

in_file = os.path.join(ROOT_DIR, 'data', '031768_t1w_deface_stx.nii.gz')

# Interface
# skullstrip = BET()
# skullstrip.inputs.in_file = in_file
# skullstrip.inputs.out_file = os.path.join('..', 'data', '031768_t1w_deface_stx_skullstrip.nii.gz')
# skullstrip.inputs.mask = True
# print(skullstrip.cmdline)
# skullstrip.run()

# workflow
skullstrip = Node(fsl.BET(in_file=in_file, mask=True), name="skullstrip")
smooth = Node(fsl.IsotropicSmooth(in_file=in_file, fwhm=4), name="smooth")
mask = Node(fsl.ApplyMask(), name="mask")
wf = Workflow(name="smoothflow") # Workflows need names too
# Now the more complicated method. Note this way you can define several connections at once,
# and you can even define several connnections between two nodes in one smalller step
wf.connect([(smooth, mask, [("out_file", "in_file")])])

wf.write_graph("workflow_graph.dot")
wf.run()


