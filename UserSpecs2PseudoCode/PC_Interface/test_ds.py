import pandas as pd

UPLOAD_FOLDER = '/media/madusha/DA0838CA0838A781/PC_Interface/Resources/filtered_zomato.csv'


def get_columns(fname):
    df = pd.read_csv(fname, nrows=0, sep='\t', delimiter=None, header='infer', names=None,
                     index_col=None, encoding="ISO-8859-1")

    attributes_real = df.columns.str.split(',')

    attr_list = []
    count = 1

    for col in attributes_real[0]:
        col_mod = str(col).strip().lower().replace(' ', '_').replace('(', '').replace(')', '')
        pair = [col_mod, col, 'column'+str(count)]
        attr_list.append(pair)
        count += 1

    return attr_list


def get_columns_old(fname):
    df = pd.read_csv(fname, nrows=0, sep='\t', delimiter=None, header='infer', names=None,
                     index_col=None, encoding="ISO-8859-1")

    attributes = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

    # attributes = df.columns.values.tolist()

    # print(len(list(df)))

    for col in attributes:
        attr = col.split(',')

    print(len(attr))
    # print(attr)
    return attr


def get_file_name(fn):
    fn_mod = fn.strip().lower().replace(' ', '_').replace('(', '').replace(')', '')
    file_name = [[fn_mod, fn, 'dataset']]

    return file_name


if __name__ == '__main__':
    file = 'Filtered Traffic.csv'
    # print(get_columns(UPLOAD_FOLDER))

    print(get_file_name(file))
