def save_stats_in_file(file, info):
    with open(file, 'a', encoding='utf8') as f:
        f.write('\n'+str(info))


def read_last_line_of_file(file):
    with open(file, 'r', encoding='utf8') as f:
        line = f.readlines()[-1].strip(' \n')
        return line

def delete_first__line_in_file(file):
    with open(file,'r', encoding='utf8') as f:
        all = f.readlines()
    if len(all) > 5:
        all.pop(0)
        with open(file,'w', encoding='utf8') as f:
            f.writelines(all)