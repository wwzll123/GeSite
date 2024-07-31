import dgl
import numpy as np
import os
import torch
import Bio.PDB as BP


letters = {'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C', 'GLU': 'E', 'GLN': 'Q', 'GLY': 'G',
           'HIS': 'H',
           'ILE': 'I', 'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S', 'THR': 'T',
           'TRP': 'W',
           'TYR': 'Y', 'VAL': 'V'}


def nor_fun(dm):
    dm_max=np.max(dm)
    dm_min=dm[dm.nonzero()].min()
    return (dm-dm_min)/(dm_max-dm_min)

def init_adjm_withDM(dm,thre=14):
    CM=dm<thre
    start,end=[],[]
    nor_dm=nor_fun(dm)
    edg_fea=None

    for raw_index,one_raw in enumerate(CM):
        index=np.where(one_raw==1)[0]
        delet_index=np.where(index==raw_index)[0][0]
        index=np.delete(index,delet_index)
        end+=index.tolist()
        start+=[raw_index]*len(index)
        one_line_dm = nor_dm[raw_index]
        if edg_fea is None:
            edg_fea=one_line_dm[index]
        else:
            edg_fea=np.concatenate((edg_fea,one_line_dm[index]),axis=0)
    g = dgl.graph((start, end),num_nodes=dm.shape[0])
    g=dgl.to_bidirected(g)
    g.edata['edg_fea']=torch.from_numpy(edg_fea)
    return g


def calc_residue_dist(residue_one, residue_two) :
    """Returns the C-alpha distance between two residues"""
    diff_vector  = residue_one["CA"].coord - residue_two["CA"].coord
    return np.sqrt(np.sum(diff_vector * diff_vector))


def calc_dist_matrix(chain_one, chain_two,AA_seq):
    """Returns a nn_saliency_matrix of C-alpha distances between two chains"""
    answer = np.zeros((len(AA_seq), len(AA_seq)),dtype=np.float32)
    row_index=0

    for row, residue_one in enumerate(chain_one):
        if (not residue_one.resname in letters):continue
        col_index=0
        for col, residue_two in enumerate(chain_two) :
            if (not residue_two.resname in letters):continue
            answer[row_index, col_index] = calc_residue_dist(residue_one, residue_two)
            col_index+=1
        row_index+=1
    return answer


def pdbToDistanceMap(pdb_id,chain_id,pdb_path):
    structure = BP.PDBParser().get_structure(pdb_id, pdb_path)
    model = structure[0]
    AA_seq=''
    target_chain=model[chain_id]
    coord_arr=None
    for one_res in target_chain:
        if one_res.resname in letters:
            AA_seq+=letters[one_res.resname]
            one_coor=np.expand_dims(one_res['CA'].coord,axis=0)
            if coord_arr is None:coord_arr=one_coor
            else:coord_arr=np.concatenate((coord_arr,one_coor),axis=0)

    dm=calc_dist_matrix(target_chain,target_chain,AA_seq)
    return dm,coord_arr,AA_seq

def bulid_graph(fea_path,pdb_path,msa_path,pdb_id,chain_id,thre=14):
    dm,coord_arr,AA_seq=pdbToDistanceMap(pdb_id=pdb_id,chain_id=chain_id,pdb_path=pdb_path)
    adjm=init_adjm_withDM(dm,thre=thre)
    fea_arr=np.loadtxt(fea_path)
    msa_fea=np.load(msa_path)
    fea=np.concatenate((fea_arr,msa_fea),axis=1)
    adjm.ndata['node_fea']=torch.from_numpy(fea)
    adjm.ndata['coord']=torch.from_numpy(coord_arr)
    return adjm