"""
@Author Janneke Grooters
@Studentnumber s4739108
"""

from typing import Dict


class FactorTable:

    def __init__(self, name, dataframe):
        self.name = name
        self.dataframe = dataframe
        self.values = dataframe.values
        self.columns = dataframe.columns
        self.observed_column = None

    def remove_observed(self, observed_name, observed_value):
        with open("log.txt", "a") as log:
            log.write("Before filtering observed:\n\n")
            log.write(f"{self.dataframe.to_string()}\n\n")
            self.dataframe = self.dataframe[self.dataframe[observed_name] != observed_value]
            log.write("After filtering observed:\n\n")
            log.write(f"{self.dataframe.to_string()}\n\n")


class FactorIdentifier:

    def __init__(self, nodes: list, probabilities: dict, observed: dict):
        """
        Initialize the class
        :param nodes:
        all the nodes in the given network
        :param probabilities:
        all the probabilites in the given network
        :param observed:
        all the evidence that is assigned in run.py
        """
        self.nodes = nodes
        self.observed = observed
        self.probabilities = probabilities

    @staticmethod
    def append_log(text: str):
        """
        This method appends to the log file with a given string.

        :param text:
        text that will be written to the file
        """
        with open("log.txt", "a") as log:
            log.write(text)

    def create_factors(self) -> Dict[str, FactorTable]:
        """
        This function create factors from the given probabiliteis in the network.
        :return:
        A dictionary with FactorTable objects used to represent the probabilities
        in a slightly different manner outside of the dataframe
        """

        factors = {}
        for key, value in self.probabilities.items():
            factors[key] = FactorTable(key, value)
        return factors

    def filter_observed(self, factors: Dict[str, FactorTable]) -> None:
        """
        This function filters out observed values out of the Factors (FactorTable objects)
        :param factors:
        A dictionary with FactorTable objects containing data from the given network
        """
        if self.observed:
            for observed_name, observed_value in self.observed.items():
                for key, factor_table in factors.items():
                    if observed_name in factor_table.columns:
                        self.append_log("------------------------------------------------------------\n\n")
                        self.append_log(f"Found a FactorTable {key} with the observed Value\n\n")
                        factor_table.remove_observed(observed_name, observed_value)
            self.append_log("------------------------------------------------------------\n\n")

    def factor_identification(self) -> Dict[str, FactorTable]:
        """
        This is the general method of the class that activates several other methods
        which perform various tasks in order to calculate the factors

        :return:
        """
        factors = self.create_factors()

        # check if observed is empty or not, if not empty then we remove observed from the FactorTables.
        if self.observed:
            self.filter_observed(factors)

            self.append_log("Check if data truly is removed from all factors:\n\n")
            for key, factor_table in factors.items():
                self.append_log(f"{factor_table.dataframe.to_string()}\n\n")
        else:
            self.append_log("Observed is empty, skipped removal process\n\n")

        return factors

