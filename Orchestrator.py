"""
@Author: Joris van Vugt, Moira Berens, Leonieke van den Bulk
Class for the implementation of the variable elimination algorithm.
"""

from Factor_Identification import FactorIdentifier
from read_bayesnet import BayesNet
from Variable_Elimination import VariableElimination


# CHANGE: renamed classname too Orchestrator as it is a better descriptor then previous name
class Orchestrator:

    def __init__(self, network: BayesNet):
        """
        Initialize the variable elimination algorithm with the specified network.
        Add more initializations if necessary.
        """
        self.network = network

    @staticmethod
    def overwrite_log(text: str):
        """
        This function overwrites the previous log file and adds a string to it.

        :param text:
        text that will be written to the file
        """
        with open("log.txt", "w") as log:
            log.write(text)

    @staticmethod
    def append_log(text: str):
        """
        This method appends to the log file with a given string.

        :param text:
        text that will be written to the file
        """
        with open("log.txt", "a") as log:
            log.write(text)

    def run(self, query, observed, elim_order):
        """
        Use the variable elimination algorithm to find out the probability
        distribution of the query variable given the observed variables
        Input:
            query:      The query variable
            observed:   A dictionary of the observed variables {variable: value}
            elim_order: Either a list specifying the elimination ordering
                        or a function that will determine an elimination ordering
                        given the network during the run
        Output: A variable holding the probability distribution
                for the query variable
        """

        # CHANGE from original code:
        # Here is where my code begins

        # Step 1: indentifying and reducing observables/evidence
        self.overwrite_log("STEP 1 : Factor Identification\n\n")

        factor_identifier = FactorIdentifier(self.network.nodes, self.network.probabilities, observed)
        factors = factor_identifier.factor_identification()  # dataframes with observed values removed

        # Step 2 Call elim_order() and run it to get the specified elimination order
        self.append_log("STEP 2 : Elimination Order\n\n")

        ordered_list = elim_order()  # elimination order in alphabetical order
        self.append_log(f"Nodes after sorting: {ordered_list}\n\n")

        # Step 3: Variable elimination
        self.append_log("STEP 3: Variable Elimination\n\n")
        VarElim = VariableElimination(factors, ordered_list)
        #VarElim.variable_elimination()

        #test sumout:
        for key, factor in factors.items():
            VarElim.sum_out(factor, key)



