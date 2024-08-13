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
- second, download the weights of all GeSite models in https://huggingface.co/anonymity/GeSite/tree/main (ESM-RBP.model, GeSite_DBS.model, and GeSite_RBS.model) and https://huggingface.co/anonymity/ESM-DBP/tree/main (ESM-DBP.model), and make sure they are located in the same folder.


# Set config
The "config.py" file should be set up correctly according to your software environment:

* config.py
 ``` 
#Need change
HHblits=r'/home/anonymity/software/hhsuite/bin/hhblits'
HHBLITS_DB=r'/home/anonymity/lib/uniclust30_2018_08/uniclust30_2018_08'
#Path of the folder contained the weights of GeSite models
model_dir=r'/home/anonymity/SCI/GeSite/exp_res/model'
PDB_dir=r'/home/anonymity/SCI/GeSite/RNA-PDB-Dataset'
threshold=0.5
 ```
 
 # Running
- You should make sure your query protein sequences in the file of './example.fasta'.
- preparing the pdb files of the proteins to be predicted and placed it at "PDB_dir".
- than, enter the following command lines on Linux System.
 ``` 
 $ python prediction.py prediciton_type device
```
- prediciton_type should be DNA or RNA. device should be cpu or cuda:0 (depend on your available hardware)
- the predicted result will be generated in file of './result'.
  
# Note
- Files of .esm_fea and .npy(ESM-MSA) are generated in './result'.
- If you already have these files, just put them into the corresponding folder, then the feature generator will not run. This will greatly reduce the prediction time.
- The protein id in your fasta file should be a PDB ID whose last letter indicates the chain to be predicted. For example 5o9z_N.
- All the best to you!

