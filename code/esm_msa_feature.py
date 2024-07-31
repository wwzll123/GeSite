#
# This file (esm_msa_feature.py) is modified by the ESM-MSA example code
# https://colab.research.google.com/github/facebookresearch/esm/blob/master/examples/contact_prediction.ipynb
#
import os,sys
import util
import esm
import torch
import string
import itertools
import numpy as np
from Bio import SeqIO
from typing import List, Tuple


esm1b,alphabet=esm.pretrained.esm_msa1b_t12_100M_UR50S()
esm1b_batch_converter=alphabet.get_batch_converter()
# translation for read sequence
deletekeys = dict.fromkeys(string.ascii_lowercase)
deletekeys["."] = None
deletekeys["*"] = None
translation = str.maketrans(deletekeys)
# read the Multiple Sequence Alignment (MSA)
def remove_insertions(sequence: str) -> str:
    """ Removes any insertions into the sequence. Needed to load aligned sequences in an MSA. """
    return sequence.translate(translation)

def read_msa(filename: str, nseq: int) -> List[Tuple[str, str]]:
    """ Reads the first nseq sequences from an MSA file, automatically removes insertions."""
    return [(record.description, remove_insertions(str(record.seq)))
            for record in itertools.islice(SeqIO.parse(filename, "fasta"), nseq)]


# inference of ESM-MSA-1b
def get_esm_msa_feats(esm1b, esm1b_batch_converter, seq_list,device):

    # convert the sequence to tokens
    esm1b_batch_labels, esm1b_batch_strs, esm1b_batch_tokens = esm1b_batch_converter(seq_list)
    esm1b=esm1b.to(device)
    esm1b_batch_tokens=esm1b_batch_tokens.to(device)
    with torch.no_grad():
        results = esm1b(esm1b_batch_tokens, repr_layers=[12], return_contacts=False)
    # esm-msa-1b sequence representation
    token_representations = results["representations"][12].mean(1)
    
    sequence_representations = []
    for i, seq in enumerate(seq_list):
        sequence_representations.append(np.array(token_representations[i, 1 : len(seq[0][1]) + 1].cpu()))

    # return the esm-msa-1d and row-attentions
    return sequence_representations[0]


def generate_data_from_file(data_path, target,device):

    # load model and read msa
    
    msa_data = [read_msa( os.path.join(data_path, target+".a3m"), 512)]

    # inference
    esm_msa_1d = get_esm_msa_feats(esm1b, esm1b_batch_converter, msa_data,device)
    np.save('./result/'+target,esm_msa_1d)
    #data = { 'esm_msa_1d':esm_msa_1d, 'row_attentions':row_attentions}
 
    # save into pkl file
    #with open( os.path.join(data_path, target+"_esm_msa.pkl"), 'wb') as f:
    #    pkl.dump(data, f, protocol = 3)

if __name__ == "__main__":



    # input args
    if len(sys.argv) != 4:
        print("USAGE ERROR")
        print("python esm_msa_feature.py fasta_path msa_path device")
        print("")
        exit()

    # generate the esm-msa features
    dicts=util.fasta2dict(sys.argv[1])
    index=1
    for one_pro in dicts:
        if os.path.exists('/home/zengww/SCI/GeSite/fea/'+one_pro+'.esm_msa'):continue
        generate_data_from_file(sys.argv[2], one_pro)
        print(one_pro+'done!')
        print(index)
        index+=1
        



