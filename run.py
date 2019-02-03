"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk

Entry point for the creation of the variable elimination algorithm in Python 3.
Code to read in Bayesian Networks has been provided. We assume you have installed the pandas package.

"""
from read_bayesnet import BayesNet
from Orchestrator import Orchestrator

if __name__ == '__main__':
    # The class BayesNet represents a Bayesian network from a .bif file in several variables
    net = BayesNet('earthquake.bif')
    # Format and other networks can be found on http://www.bnlearn.com/bnrepository/
    
    # These are the variables read from the network that should be used for variable elimination
    # print("Nodes:")
    # print(net.nodes)
    # print("Values:")
    # print(net.values)
    # print("Parents:")
    # print(net.parents)
    # print("Probabilities:")
    # print(net.probabilities)

    # Make your variable elimination code in a seperate file: 'variable_elim'.
    # You can call this file as follows:
    ve = Orchestrator(net)

    # Set the node to be queried as follows:
    query = 'Alarm'

    # The evidence is represented in the following way (can also be empty when there is no evidence):
    #evidence = {'Burglary': 'True', 'Earthquake': 'False'}
    evidence = {}

    # Determine your elimination ordering before you call the run function. The elimination ordering   
    # is either specified by a list or a heuristic function that determines the elimination ordering
    # given the network. Experimentation with different heuristics will earn bonus points. The elimination
    # ordering can for example be set as follows:

    # CHANGE from original code:
    # Remade elim_order into a function that orders the nodes by name.
    def elim_order():
        with open("log.txt", "a") as log:
            log.write(f"Nodes before sorting: {str(net.nodes)}\n")
            return sorted(net.nodes)

    # Call the variable elimination function for the queried node given the
    # evidence and the elimination ordering as follows:
    ve.run(query, evidence, elim_order)
