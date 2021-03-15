# Import BET from the FSL interface
from nipype.interfaces.fsl import BET
# Import the Node module
from nipype import Node

# Create Node
bet = Node(BET(frac=0.3), name='bet_node')
# Specify node inputs
bet.inputs.in_file = '/data/ds000114/sub-01/ses-test/anat/sub-01_ses-test_T1w.nii.gz'
bet.inputs.out_file = '/output/node_T1w_bet.nii.gz'
res = bet.run()
