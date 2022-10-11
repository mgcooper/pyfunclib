from collections import OrderedDict
def json2csv(input_f, output_f):
    """ Convert JSON to CSV """

    input_data = json.load(input_f, object_pairs_hook=OrderedDict)

    if isinstance(input_data, list):
        list_of_dicts = input_data
        fieldnames = list_of_dicts[0].keys()

    elif isinstance(input_data, dict):
        dict_of_lists = input_data
        fieldnames = dict_of_lists.keys()

        # Dict of lists to list of dicts
        # Assume all lists are same length
        list_len = len(dict_of_lists.values()[0])
        list_of_dicts = [
            {k: v[i] for k, v in dict_of_lists.items()}
            for i in range(list_len)
        ]

    with open(output_f, 'wb') as fou:
        w = csv.DictWriter(fou, fieldnames, lineterminator='\n')
        w.writeheader()
        w.writerows(list_of_dicts)