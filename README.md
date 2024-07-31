# GeSite
The data and standalone program of GeSite.
# Pre-requisite:
- Python(3), numpy(1.20 or higher), pandas (1.4.2 or higher), pytorch(1.5 or higher)
- HHblits software (https://github.com/soedinglab/hh-suite)
- Uniclust30 database (https://uniclust.mmseqs.com/)
- ESM2 (https://github.com/facebookresearch/esm)
- Linux system
# Installation:
- First, download the source code in this repository.
- second, download the weights of all GeSite models in https://huggingface.co/zengwenwu/GeSite/tree/main, and make sure they are located in the same folder.


# Set config
The "config.ini" file should be set up correctly according to your software environment:

* config.py
 ``` 
#Need change
HHblits=r'/home/zengww/software/hhsuite/bin/hhblits'
HHBLITS_DB=r'/home/zengww/lib/uniclust30_2018_08/uniclust30_2018_08'
model_dir=r'/home/zengww/SCI/GeSite/exp_res/model'
PDB_dir=r'/home/zengww/SCI/GeSite/RNA-PDB-Dataset'
threshold=0.5
 ```
 
 # Running
- You should make sure your query protein sequences in the file of './workFolder/seqs.fa'.
- than, enter the following command lines on Linux System.
 ``` 
 $ python prediction.py prediciton_type device
``` 
- the predicted result will be generated in file of './workFolder/querys.jun_res'.
- The first column is the prediction result, 0 means non-DBP, 1 means DBP. The second column is the probability of being predicted as a positive sample. The third column is the probability of being predicted as a negative sample.
  
# Note
- Files of .esm_fea and .npy(ESM-MSA) are generated in './result'.
- If you already have these files, just put them into the corresponding folder, then the feature generator will not run. This will greatly reduce the prediction time.
- If you have any question, please send email to wwz_cs@126.com.
- All the best to you!

# Reference
[1] Wenwu Zeng, Liangrui Pan, Dafeng Lv, Liwen Xu, and Shaoliang Peng. Accurate nucleic acid-binding residue identification based on domain-adaptive protein language model and explainable geometric deep learning. Submitted.
 

