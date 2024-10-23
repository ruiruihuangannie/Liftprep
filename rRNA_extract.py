'''
python3 rRNA_extract.py sample_inputs/CHM13_canonical.gff rRNA_only.with_root.gff
'''
import sys
import utils
from tqdm import tqdm

def main(in_fn, out_fn):
    rRNA_add_fake_root(open(in_fn, 'r'), open(out_fn, 'w'))

def rRNA_add_fake_root(in_fh, out_fh):
    g_lst, rRNA_lst = dict(), list()
    for line in tqdm(in_fh.readlines(), desc='processed gff entries'):
        row = line.rstrip().split('\t')
        if len(row) < 9:
            continue
        f_chm, f_type, f_annot = row[0], row[2], row[8]
        if f_type == 'gene':
            g_id, g_type = utils.extract_parent_annotation(f_annot)
            if g_type == 'rRNA':
                if f_chm not in g_lst:
                    g_lst[f_chm] = tuple([line])
                else:
                    g_lst[f_chm] += tuple([line])
        elif f_type == 'rRNA':
            rRNA_lst.append(line)
    in_fh.close()

    sorted_dict = dict()
    cnt = 0
    for k, v in g_lst.items():
        sorted_dict[k] = sorted(v)
        cnt += len(v)
    print(f'{cnt} rDNA entries in total.')

    fake_root_lst = list()
    cnt = 1
    for chm, tup in tqdm(sorted_dict.items(), desc='Adding fake root'):
        if chm not in ['chr13','chr14','chr15','chr21','chr22']:
            continue
        i = 0
        while i < len(tup):
            row = tup[i].rstrip().split('\t')
            if '18S' in row[8] and i + 2 < len(tup):
                nxt = tup[i+1].rstrip().split('\t')
                nxt2= tup[i+2].rstrip().split('\t')
                if '5.8S' in nxt[8] and '28S' in nxt2[8]:
                    id_unit = "unit_" + str(cnt)
                    line = '\t'.join(
                        [row[0], row[1], "rRNA_full_unit",
                         row[3], nxt2[4],
                         row[5], row[6], row[7], 
                         'ID=' + id_unit]
                    ) + '\n'
                    fake_root_lst.append(line)  # list of all roots
                    for j in range(3):
                        tup[i + j] = tup[i + j].rstrip() + ';Parent=' + id_unit + '\n'
                    cnt += 1
                    i += 2
            i += 1
    print(f'Added {cnt - 1} roots for acrocentric rDNAs.')

    for line in tqdm(fake_root_lst, desc= 'Write roots to file'):
        out_fh.write(line)
    for k, v in tqdm(sorted_dict.items(), desc = 'Write gene-level features to file'):
        for line in v:
            out_fh.write(line)
    for line in tqdm(rRNA_lst, desc='Write rDNAs to file'):
        out_fh.write(line)
    out_fh.close()

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
