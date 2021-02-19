from nipype.interfaces.freesurfer import SurfaceSmooth
smoother = SurfaceSmooth()
smoother.inputs.in_file = "{hemi}.func.mgz"
smoother.iterables = [("hemi", ['lh', 'rh']),
                      ("fwhm", [4, 8]),
                      ("subject_id", ['sub01', 'sub02', 'sub03',
                                      'sub04', 'sub05', 'sub06']),
                      ]
# smoother.run(mode='parallel')
print(smoother.cmdline)