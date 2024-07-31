import egnn_clean
import torch
import esm
import os
import pandas as pd
import esm_msa_feature
import util
import config
import bulid_protein_graph
import numpy as np


fasta_path='./example.fasta'
prediction_type='RNA'
device='cpu'


# esm-msa feature generate
print('1. Running HHblits...')
util.get_MSA(fasta_path,config.HHblits,config.HHBLITS_DB)
pro_dicts=util.fasta2dict(fasta_path)

print('2. Running ESM-MSA...')
for one_pro in pro_dicts:
    if os.path.exists('./result/'+one_pro+'.npy'):continue
    esm_msa_feature.generate_data_from_file('./result',one_pro,device)

#load esm model
esm_dbp_model=esm.ESM2()
alphabet = esm.data.Alphabet.from_architecture("ESM-1b")

if prediction_type == 'DNA':
    ESM_model_path=config.model_dir+os.sep+'ESM-DBP.model'
    EGNN_path=config.model_dir+os.sep+'GeSite_DBS.model'
elif prediction_type == 'RNA':
    ESM_model_path=config.model_dir+os.sep+'ESM-RBP.model'
    EGNN_path=config.model_dir+os.sep+'GeSite_RBS.model'
else:
    raise ValueError('Prediction type must be DNA or RNA!')


esm_model = torch.nn.DataParallel(esm_dbp_model)
esm_model.load_state_dict(torch.load(ESM_model_path, map_location=lambda storage, loc: storage))
esm_model.to(device)
esm_model.eval()

def get_one_protein_esm_fea(protein_name,seq):
    #print("Generate feature representation of {0}...".format(protein_name))
    data = [(protein_name, seq)]
    batch_converter = alphabet.get_batch_converter()
    batch_labels, batch_strs, batch_tokens = batch_converter(data)
    # Extract per-residue representations (on device)
    with torch.no_grad():
        batch_tokens=batch_tokens.to(device)
        #batch*seq_len*fea_dim
        results = esm_model(batch_tokens, repr_layers=[33], return_contacts=False)
        token_representations = torch.squeeze(results["representations"][33])
        return token_representations[1:-1]

#load
GraphModel = egnn_clean.EGNN(in_node_nf=2048, hidden_nf=512, out_node_nf=2, in_edge_nf=1)
GraphModel.load_state_dict(torch.load(EGNN_path, map_location=lambda storage, loc: storage))
GraphModel.to(device)
GraphModel.eval()


print('3. Prediction start...')
for one_pro in pro_dicts:
    res_dict={}
    esm_fea=get_one_protein_esm_fea(one_pro,pro_dicts[one_pro])
    np.savetxt('./result/'+one_pro+'.esm_fea',esm_fea,fmt='%.12f')
    one_graph=bulid_protein_graph.bulid_graph('./result/'+one_pro
        +'.esm_fea',config.PDB_dir+os.sep+one_pro+'.pdb','./result/'+one_pro+'.npy',one_pro,one_pro[-1])

    node_fea, coord = one_graph.ndata['node_fea'], one_graph.ndata['coord']
    edg_fea = one_graph.edata['edg_fea']
    edges_tuple = list(one_graph.all_edges())
    edges_tuple[0], edges_tuple[1] = edges_tuple[0].to(device), edges_tuple[1].to(device)
    inputs = node_fea.float()
    inputs, coord, edg_fea = inputs.to(device), coord.to(device), edg_fea.to(device)
    edg_fea = torch.unsqueeze(edg_fea, dim=1)
    with torch.no_grad():
        out, out_coord = GraphModel(inputs, coord, edges_tuple, edg_fea)
        out = torch.squeeze(out)#这里应该是seq_len*2
        out = torch.softmax(out, dim=1)
    out=out.detach().cpu().numpy()[:,1]
    res_dict['amino acid']=list(pro_dicts[one_pro])
    res_dict['binding probability']=out
    res_dict['binding binary']=(out>=config.threshold)
    pd.DataFrame(res_dict).to_csv('./result/'+one_pro+'.csv')

print('4. Prediction is over!')