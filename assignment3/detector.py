#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#         ____ ____    __________ _                                            #
#        / ___/ ___|  |___ /___ // |                                           #
#       | |   \___ \    |_ \ |_ \| |                                           #
#       | |___ ___) |  ___) |__) | |                                           #
#        \____|____/  |____/____/|_|                                           #
#        _   ___        __    _  _     _____                                   #
#       | | | \ \      / /  _| || |_  |___ /                                   #
#       | |_| |\ \ /\ / /  |_  ..  _|   |_ \                                   #
#       |  _  | \ V  V /   |_      _|  ___) |                                  #
#       |_| |_|  \_/\_/      |_||_|   |____/                                   #
################################################################################
# Imports
import getopt
import sys
import os
import string
import ast
from math import log10

#global varibles
i = []
t = []
i_f = []
t_f = []
vocab = {}
vocab_list = []
total_sarcastic = 0

def usage():
    print sys.argv[0] + "  <it>||<input,train> [hv] [help]"
    print "\t-i,--input\t\tInput file"
    print "\t-t,--train\t\tTraining file"
    print "\t-v\t\t\tVerbose output"
    print "\t-vv\t\t\tVery Verbose output"
    print "\t-h,--help\t\tPrint usage message"

def data_print(l):
    for tup in l:
        print str(tup[1]) + "\t" + tup[0]

def output(verbose):
    global vocab
    global i
    global t
    global i_f
    global t_f
    global total_sarcastic

    # Write to files
    pre_train = open('preprocessed_train.txt', 'wb')
    pre_test  = open('preprocessed_test.txt', 'wb')

    if verbose: print ', '.join(sorted(vocab.keys())) + ', classlablel'
    pre_train.write(', '.join(sorted(vocab.keys())) + ', classlabel\n')
    for tup in t:
        tl = sorted(tup[0].split(' '))
        if '' in tl: tl.remove('')
        temp = []
        for word in sorted(vocab.keys()):
            if word in tl:
                if verbose: print'1,',
                pre_train.write('1,')
                temp.append(1)
            else:
                if verbose: print '0,',
                pre_train.write('0,')
                temp.append(0)
            vocab_list.append(word)

        if verbose: print tup[1]
        if tup[1]: total_sarcastic += 1
        pre_train.write(str(tup[1]) + '\n')
        temp.append(tup[1])
        t_f.append(temp)

    pre_test.write(', '.join(sorted(vocab.keys())) + ', classlabel\n')
    for tup in i:
        tl = sorted(tup[0].split(' '))
        if '' in tl: tl.remove('')
        temp = []
        #print ', '.join(tl)
        for word in sorted(vocab.keys()):
            if word in tl:
                if verbose: print'1,',
                pre_test.write('1,')
                temp.append(1)
            else:
                if verbose: print '0,',
                pre_test.write('0,')
                temp.append(0)
        if verbose: print tup[1]
        pre_test.write(str(tup[1]) + '\n')
        temp.append(tup[1])
        i_f.append(temp)

    pre_train.close()
    pre_test.close()

def preprocess(input_file, train_file, verbose):
    global i
    global t
    global bag
    global vocab
    global vocab_list

    if verbose:
        print "Input file: " + str(input_file)
        print "Train file: " + str(train_file)

    # Sanitize input files
    with open(input_file) as f:
        for line in f:
            temp = line.split(',')
            if len(temp) == 2:
                i.append(((temp[0].translate(None, string.punctuation)).lower(),bool(int(temp[1].strip(temp[1].translate(None, string.digits))))))

    # Read in the training file and normalize
    with open(train_file) as f:
        for line in f:
            temp = line.split(',')
            if len(temp) == 2:
                t.append(((temp[0].translate(None, string.punctuation)).lower(),bool(int(temp[1].strip(temp[1].translate(None, string.digits))))))

    if verbose > 1:
        print 'Test data:'
        data_print(i)
        print 'Train data:'
        data_print(t)


    for tup in t:
        for word in tup[0].split(' '):
            if word and not word in vocab.keys():
                if tup[1]:
                    # Initialize value
                    vocab[word.lower()] = [1, 1, 0]
                else:
                    # Initialize value
                    vocab[word.lower()] = [1, 0, 1]
            elif word in vocab.keys():
                if tup[1]:
                    # Increment word counter
                    vocab[word][0] += 1
                    # Increment sarcastic counter
                    vocab[word][1] += 1
                else:
                    # Increment word counter
                    vocab[word][0] += 1
                    # Increment serious counter
                    vocab[word][2] += 1



    # Alphebetically sort the words
    if verbose > 1: print vocab

    # Print to files
    output(verbose)

def classification(verbose):
    pr = {}
    pr_true = float(total_sarcastic) / float(len(t_f))
    pr_false = float(len(t_f) - total_sarcastic) / float(len(t_f))
    result = open('results.txt', 'wb')

    if verbose:
        print "vocab: ", vocab

    for key, value in vocab.iteritems():
        # Get the probability of each word [TT,TF,FT,FF]
        pr[key] = [float(value[1]) / float(value[0]), float(value[1]) / float(value[0]), float(value[2]) / float(value[0]), float(value[2]) / float(value[0])]

    if verbose:
        print t_f
        print pr

    train = True
    # For feature in feature list
    for data_set in [t_f, i_f]:
        ct = 0
        for f in data_set:
            # Probability that the sentance is sarcastic
            true_prod = 1.0
            false_prod = 1.0
            for fet in xrange(len(f)-1):
                if f[fet]:
                    if vocab_list[fet] in pr.keys():
                        true_prod += pr[vocab_list[fet]][0]
                        false_prod += pr[vocab_list[fet]][3]

            if true_prod > false_prod:
                if verbose: print 'true:', true_prod
                if f[-1]: ct += 1
            else:
                if verbose: print 'false: ', false_prod
                if not f[-1]: ct += 1
        if train:
            print 'Training: ', (float(ct)/float(len(data_set)))
            result.write('Training: ' + str(float(ct)/float(len(data_set))) + '%\n')
            print 'Data Set Size: ', len(data_set)
            result.write('Data Set Size: ' + str(len(data_set)) + '\n')
            print 'Number Correct: ', ct
            result.write('Number Correct: ' + str(ct) + '\n')
            result.write('################################################################################\n')
            print '################################################################################'
            train = False
        else:
            print 'Test: ', (float(ct)/float(len(data_set)))
            result.write('Test: ' + str(float(ct)/float(len(data_set))) + '%\n')
            print 'Data Set Size: ', len(data_set)
            result.write('Data Set Size: ' + str(len(data_set)) + '\n')
            print 'Number Correct: ', ct
            result.write('Number Correct: ' + str(ct) + '\n')


def main():

    # Get all command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:t:vh", ["help", "input=", "train="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)



    input_file = 'test_text.txt'
    train_file = 'training_text.txt'
    verbose = 0
    for o, a in opts:
        if o == "-v":
            verbose = verbose + 1
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--input"):
            input_file = a
        elif o in ("-t", "--train"):
            train_file = a
        else:
            assert False, "unhandled option"
            usage()
            sys.exit(2)

    # Check if all required arguments are provided
    if input_file == None or train_file == None:
        usage()
        sys.exit(3)

    # Check if all data files are present on the host
    if os.path.isfile(input_file) and os.path.isfile(train_file):
        # Preprocess the data from the files provided
        preprocess(input_file, train_file, verbose)
        # Classify the normalized data
        classification(verbose)
    else:
        print "One or more of the files provided are not present"
        sys.exit(4)


if __name__ == "__main__":
        main()
