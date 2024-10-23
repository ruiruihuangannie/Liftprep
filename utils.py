import sys
import os
from tqdm import tqdm

def field_kv_pairs(string):
  fields = string.rstrip().split(';')
  pairs = dict()
  for field in fields:
    k, v = field.rstrip().split('=')
    pairs[k] = v
  return pairs

def extract_parent_annotation(string):
  kv = field_kv_pairs(string)
  return kv['ID'], kv['gene_biotype']

def extract_child_annotation(string):
  kv = field_kv_pairs(string)
  return kv['ID'], kv['Parent']

def extract_gff(in_fh, out_fh, extract_VDJ=False, extract_rDNA=False, extract_chrY=False):
  """
  Process the GFF file and extract VDJ, rDNA, and/or chrY regions based on user selection.
  The file is processed once, and the relevant regions are written to the output.
  """
  g_lst, vdj_lst, exon_lst = list(), list(), list()
  rDNA_lst = list()

  for line in tqdm(in_fh.readlines(), desc="Processed gff entries"):
    kept = False
    fields = line.rstrip().split('\t')
    if len(fields) < 9:
      continue

    f_type, f_annot = fields[2], fields[8]

    # Extract chrY-related entries
    if extract_chrY and fields[0] == 'chrY':
      out_fh.write(line)
      continue

    # Extract VDJ-related entries
    if extract_VDJ and f_type in ['gene', 'pseudogene']:
      g_id, g_type = extract_parent_annotation(f_annot)
      if g_type in ["V_segment", "D_segment", "J_segment", "J_segment_pseudogene", "V_segment_pseudogene"]:
        g_lst.append(g_id)
        kept = True
    elif extract_VDJ and f_type in ['V_gene_segment', 'D_gene_segment', 'J_gene_segment', 'exon']:
      t_id, t_parent = extract_child_annotation(f_annot)
      if t_parent in g_lst:
        vdj_lst.append(t_id)
        kept = True
      elif t_parent in vdj_lst:
        exon_lst.append(t_id)
        kept = True

    # Extract rDNA-related entries
    if extract_rDNA and f_type == 'gene':
      g_id, g_type = extract_parent_annotation(f_annot)
      if g_type == 'rRNA':
        g_lst.append(g_id)
        kept = True
    elif extract_rDNA and f_type == "rRNA":
      t_id, t_parent = extract_child_annotation(f_annot)
      if t_parent in g_lst:
        rDNA_lst.append(t_id)
        kept = True
    # Write the line if it matched any of the criteria
    if kept:
        out_fh.write(line)
  in_fh.close()
  out_fh.close()


def discard_gff(in_fh, out_fh, discard_VDJ=False, discard_rDNA=False, discard_chrY=False):
  """
  Process the GFF file and extract VDJ, rDNA, and/or chrY regions based on user selection.
  The file is processed once, and the relevant regions are written to the output.
  """
  g_lst, vdj_lst, exon_lst = list(), list(), list()
  rDNA_lst = list()

  for line in tqdm(in_fh.readlines(), desc="Processed gff entries"):
    fields = line.rstrip().split('\t')
    if len(fields) < 9:
      continue

    f_type, f_annot = fields[2], fields[8]

    if discard_chrY and fields[0] == 'chrY':
      continue

    if discard_VDJ and f_type in ['gene', 'pseudogene']:
      g_id, g_type = extract_parent_annotation(f_annot)
      if g_type in ["V_segment", "D_segment", "J_segment", "J_segment_pseudogene", "V_segment_pseudogene"]:
        g_lst.append(g_id)
        continue
    elif discard_VDJ and f_type in ['V_gene_segment', 'D_gene_segment', 'J_gene_segment', 'exon']:
      t_id, t_parent = extract_child_annotation(f_annot)
      if t_parent in g_lst:
        vdj_lst.append(t_id)
        continue
      elif t_parent in vdj_lst:
        exon_lst.append(t_id)
        continue

    if discard_rDNA and f_type == 'gene':
      g_id, g_type = extract_parent_annotation(f_annot)
      if g_type == 'rRNA':
        g_lst.append(g_id)
        continue
    elif discard_rDNA and f_type == "rRNA":
      t_id, t_parent = extract_child_annotation(f_annot)
      if t_parent in g_lst:
        rDNA_lst.append(t_id)
        continue
    out_fh.write(line)
  in_fh.close()
  out_fh.close()

def make_canonical(mp, lst):
  lst_name = list()

  for fn in lst:
    with open(fn, 'r') as fh:
      name = fn
      if any(ext in fn for ext in ['gff', 'gtf']):
          name = f"{fn.split('.')[0]}_canonical.gff"
          if os.path.isfile(name):
            print(f'[Info]: {name} exists, moving on...')
          else:
            gff_sub(mp, fh, open(name,'w'))
      elif any(ext in fn for ext in ['fna', 'fa', 'fasta']):
          name = f"{fn.split('.')[0]}_canonical.fna"
          if os.path.isfile(name):
            print(f'[Info]: {name} exists, moving on...')
          else:
            fna_sub(mp, fh, open(name,'w'))
      lst_name.append(name)
  return lst_name

def gff_sub(mp, fh, out_fh):
  cnt = 0
  for ln in tqdm(fh.readlines(), desc="Processed gff entries"):
    fields = ln.rstrip().split('\t')
    if fields[0] in mp:
      fields[0] = mp[fields[0]]
      cnt += 1
    out_fh.write('\t'.join(fields) + '\n')
  print(f'[Info]: Successfully canonicalized {cnt} entries.')

def fna_sub(mp, fh, out_fh):
  cnt = 0
  for ln in tqdm(fh.readlines(), desc="Processed fna entries"):
    if ln.startswith('>'):
      fields = ln.rstrip().split(' ')
      if fields[0][1:] in mp:
        fields[0] = '>' + mp[fields[0][1:]]
        cnt += 1
      out_fh.write(f'{fields[0]}\n')
    else:
      out_fh.write(ln)
  print(f'[Info]: Successfully canonicalized {cnt} entries.')

      
if __name__ == '__main__':
  extract_gff(open(sys.argv[1], 'r'), open(sys.argv[2], 'w'), extract_VDJ=True)