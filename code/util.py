import os

def fasta2dict(file_path):
    fi=open(file_path,'r')
    dicts={}
    while True:
        oneLine=fi.readline()
        twoLine=fi.readline()
        if not oneLine:break
        dicts[oneLine[1:-1]]=twoLine.replace('\n','')
    fi.close()
    return dicts


def get_MSA(fasta_path,hhblits_bin,HHBLITS_DB):
    pro_dicts=fasta2dict(fasta_path)
    for one_pro in pro_dicts:
        fi=open('./{0}.fasta'.format(one_pro),'w')
        fi.write('>'+one_pro+'\n'+pro_dicts[one_pro]+'\n')
        fi.close()
        result_path ='./result/{0}.a3m'.format(one_pro)
        if os.path.exists(result_path):continue

        hhm_cmd = hhblits_bin + ' -i ./{0}.fasta'.format(one_pro) + ' -d ' + HHBLITS_DB + ' -n ' + str(3) + ' -e ' + str(
            0.1)+' -oa3m '+result_path+' -cpu 10'
        os.system(hhm_cmd)
        os.remove('./{0}.fasta'.format(one_pro))
        os.remove('./{0}.hhr'.format(one_pro))