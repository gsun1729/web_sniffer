import sys
import argparse
from plate2genotype import process_txtfile

def get_args(args):
    parser = argparse.ArgumentParser(description = 'Given two lists of genes, find intersection')
    parser.add_argument('-i1',
                        dest = 'input1',
                        help = 'input queries 1',
                        required = True)
    parser.add_argument('-i2',
                        dest = 'input2',
                        help = 'input queries 2',
                        required = True)
    parser.add_argument('-o',
                        dest = 'output_path',
                        help = 'output filepath',
                        required = False)

    return vars(parser.parse_args())

def main(args):
    options = get_args(args)
    set1 = options['input1']
    set2 = options['input2']
    write_path = options['output_path']

    lower_flatten =  lambda list: [item.lower() for sublist in list for item in sublist]
    set1_data = lower_flatten(process_txtfile(set1))
    set2_data = lower_flatten(process_txtfile(set2))

    s12_difference = list(set(set1_data)-set(set2_data))
    s21_difference = list(set(set2_data)-set(set1_data))
    intersection = list(set(set1_data).intersection(set2_data)))

    file = open(write_path, 'w')
    file.write("Set1 Path: {}\n".format(set1))
    file.write("Set2 Path: {}\n".format(set2))
    file.write("Set1 Size: {}\n".format(len(set(set1_data))))
    file.write("Set2 Size: {}\n".format(len(set(set1_data))))
    file.write("Set1, Set2 Intersection size: {}\n".format())


if __name__ == "__main__":
    main(sys.argv)
