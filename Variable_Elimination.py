"""
@Author Janneke Grooters
@Studentnumber s4739108
"""

import pandas as pd
from Factor_Identification import FactorTable

class VariableElimination:

    def __init__(self, factors, ordered_list):
        self.factors = factors
        self.ordered_list = ordered_list

    @staticmethod
    def append_log(text: str):
        """
        This method appends to the log file with a given string.

        :param text:
        text that will be written to the file
        """
        with open("log.txt", "a") as log:
            log.write(text)

    def sum_out(self, factor, variable):
        """
        removes variable column, sorts factor and then merges each two subsequent rows to create a new factor.

        :param factor:
        This parameter is of type FactorTable, defined in Factor_Identification.py.

        :param variable:
        This parameter is the key for the dataframe defined in the probabilities.

        :return:
        This method return a new FactorTable object which is created out of the factor parameter.
        """

        self.append_log(f"Sum out over factor for variable; {variable}: \n {factor.dataframe}\n\n")
        factor = factor.dataframe.drop(columns=[variable])
        columns = list(factor)
        factor = factor.sort_values(by=columns)
        new_df = pd.DataFrame(columns=columns)

        if len(factor.index) > 2:
            # loop over the rows, take each even and corresponding odd index and sum their probabilities
            for i in range(0, int((len(factor.index)/2))):
                new_row = []
                prob1 = factor.iloc[i * 2, len(columns) - 1]
                prob2 = factor.iloc[i * 2 + 1, len(columns) - 1]
                new_prob = (prob1 + prob2)

                # add truth values to new row
                for j in range(0, len(columns)-1):
                    new_row.append(factor.iloc[i*2, j])

                # add new probabilty value to new row
                new_row.append(new_prob)

                # convert row to a dataframe and add to the new factor
                temp_factor = pd.DataFrame([new_row], columns=columns)
                new_df = new_df.append(temp_factor, ignore_index=True)

            # convert dataframe to a FactorTable
            new_factor = FactorTable(variable,new_df)

            self.append_log("------------------------------------------------------------\n\n")
            self.append_log(f"New factor after sum out: \n {new_factor.dataframe} \n\n")
            return new_factor

        else:
            self.append_log("Factor reduced to empty set after summing out \n\n")
            self.append_log("------------------------------------------------------------\n\n")
            return

    def factor_multiplication(self, factor_list):
        """
        multiplies all factors in a given list and returns a single factor

        :param factor_list:
        This is a list containing multiple FactorTable objects. FactorTable is defined in Factor_Identification.py

        :return:
        """

        # TODO: implement factor multiplication
        factor_list = [factor_list[0]]
        return factor_list

    def variable_elimination(self):
        """
        This method implements the sum_out() and factor_multiplication() methods

        Its main goal is looping through the whole netowrk and using the above
        mentioned methodes to eilimnate al variables.

        :return:
        """
        for var in self.ordered_list:
            elim_factors = []
            keys = []

            # search self.factors for factors that contain variable, remove from self.factors and add to new list:
            for key, factorTable in self.factors.items():
                if factorTable:
                    if var in factorTable.columns:
                        elim_factors.append(factorTable)
                        keys.append(key)

            for key in keys:
                self.factors.pop(key)

            if elim_factors:
                if len(elim_factors) > 1:
                    elim_factors = self.factor_multiplication(elim_factors)

                new_factor = self.sum_out(elim_factors[0], var)

                if new_factor:
                    self.factors[new_factor.name] = new_factor

        if self.factors:
            return self.factors[next(iter(self.factors))]
        else:
            self.append_log("there are no factors to return")
