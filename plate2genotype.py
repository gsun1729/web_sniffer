import urllib2
import os
import csv
import sys
import argparse
from bs4 import BeautifulSoup


def get_args(args):
    parser = argparse.ArgumentParser(description = "Script for correlating plate number with genotype")
    parser.add_argument('-mode',
                        dest = 'mode',
                        help = 'processing mode',
                        required = True,
                        default = 'single')
    parser.add_argument('-I',
                        dest = 'input',
                        help = 'input ID file or name',
                        required = True)
    parser.add_argument('-o',
                        dest = 'output_path',
                        help = 'output filepath',
                        required = False)
    parser.add_argument('-database',
                        dest = 'LUT',
                        help = 'database path',
                        required = True)
    return vars(parser.parse_args())


def search(query):
    for r_index, row in enumerate(lookup_database):
        if row[-1] == query:
            return row[1:3]


def process_txtfile(filepath):
    file = open(filepath, 'r')
    file_data = file.readlines()
    output = []
    for indx, item in enumerate(file_data):
        output.append(file_data[indx].rstrip('\n').split('\t'))
    file.close()
    return output


def process(args):
    options = get_args(args)
    mode = options['mode']
    query = options['input']
    database_path = options['LUT']
    if mode != 's' and mode != 'b':
        raise Exception('-mode should be specified as either \'s\' or \'b\'')

    global lookup_database
    lookup_database = process_txtfile(database_path)

    if mode == 's':
        gene_name, strain = search(query)
        print("Query:\t{}\nSystemic Name:\t{}\nStrain:\t{}\n".format(query, gene_name, strain))
    else:
        output_path = options['output_path']
        if output_path == None:
            raise Exception('Output Filepath required [-o]')
        results_file = open(output_path, 'w')
        query_data = process_txtfile(query)
        lower_flatten =  lambda list: [item.lower() for sublist in list for item in sublist]
        query_data = lower_flatten(query_data)

        for query in query_data:
            for r_index, row in enumerate(lookup_database):
                found = False
                if row[-1] == query.lower():
                    gene_name, strain = search(query)
                    found = True
                    results_file.write("%s\t%s\t%s\n" % (query, gene_name, strain))
                    break
            if not found:
                results_file.write("%s\t%s\t%s\n" % (query, "NA", "NA"))
        results_file.close()


# https://www.yeastgenome.org/search?q=YBR011C&is_quick=true
if __name__ == "__main__":
    process(sys.argv)
