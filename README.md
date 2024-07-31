# GeSite
The data and standalone program of GeSite.
# Pre-requisite:
- Python(3), numpy(1.20 or higher), pandas (1.4.2 or higher), pytorch(1.5 or higher)
- HHblits software (https://github.com/soedinglab/hh-suite)
- Uniclust30 database (https://uniclust.mmseqs.com/)
- ESM2 (https://github.com/facebookresearch/esm)
- Linux system
# Installation:
- First, download compressed packages in (https://github.com/wwzll123/TPSO/tree/main/Standalone_Program)
- second, download the FileUnion.jar in (https://github.com/wwzll123/TPSO/tree/main/FileSplit)
- third, union these compressed packages using FileUnion.jar by typing the following command
```
# [packages folder path] should be the path that contains files of TPSO_DBP.tar.gz_0 ~ TPSO_DBP.tar.gz_20.
$ java -jar FileUnion.jar [packages folder path] ./TPSO_DBP.tar.gz
```
- fourth, uncompress the generated file of TPSO_DBP.tar.gz.
- fifth, provide executable permissions for file of './jar/tools/blast-2.2.26/blastpgp'.


# Set config
The files of “Config.properties” and "config.ini" should be set as follows:

* Config.properties
 ```
DBS_PRED_MODEL=./jar/model/dbs/dbs.mod
BLAST_BIN_DIR=./jar/tools/blast-2.2.26
BLASTPGP_EXE_PATH=./jar/tools/blast-2.2.26/blastpgp

#Need change
SANN_RUNNER_PATH=Absolute_Path_SANN_Installtion/SANN/sann/bin/sann.sh
BLASTPGP_DB_PATH=Absolute_Path_nr_Installtion/nr
```
* config.ini
 ``` 
[PATH]

#Need change
TPSO_HOME=/data0/junh/stu/wenwuzeng/software/TPSO_DBP
PSIPRED_HOME=Absolute_Path_PSIPRED_Installtion/psipred321
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
 

