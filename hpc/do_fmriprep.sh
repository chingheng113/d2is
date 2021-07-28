singularity run ./fmriprep.simg \
    ./f_test ./f_test/derivatives \
    participant \
    --participant-label 01 \
    --skip-bids-validation \
    --md-only-boilerplate \
    --fs-license-file ./f_test/license.txt \
    --fs-no-reconall \
    --output-spaces MNI152NLin2009cAsym:res-2 \
    --nthreads 4 \
    --stop-on-first-crash \
    -w ./f_test