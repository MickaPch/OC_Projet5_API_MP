"""Program static methods"""
import sys
import json


class Statics():
    """Static methods"""

    @staticmethod
    def json_dict(file):
        """
        Read the parameters from JSON file
        and convert into dict
        """

        with open(file, 'r') as json_file:
            return json.load(json_file)

    @staticmethod
    def input_y_n(msg):
        """
        User choice between YES or NO.
        'exit' for quit program.
        """

        while True:
            choice = input(msg)

            # For each user input, user can quit typing 'exit'
            if choice.lower() == "exit":
                sys.exit()

            # Accept 'y' or 'yes', lower or upper
            elif choice.upper() in ('Y', 'YES'):
                choice = True
                break

            # Accept 'n' or 'no', lower or upper
            elif choice.upper() in ('N', 'NO'):
                choice = False
                break

        return choice

    @staticmethod
    def input_list(list_choices, master=""):
        """
        Checks if user choice is valid and return choice.
        "master" is used when program need 0-option
        (Show all products)
        Program may be quit typing 'exit'.
        """

        if master == "":
            dict_choices = {}
        else:
            dict_choices = {0: master}


        i = 0
        while i < len(list_choices):
            dict_choices[i + 1] = list_choices[i]
            i += 1

        list_number = sorted(dict_choices.keys())

        for i in list_number:
            print("  - {}. {}".format(str(i), dict_choices[i]))

        while True:
            choice = input('\n>>> ')
            if choice.lower() == "exit":
                sys.exit()
            try:
                # Check if input is a number
                # And if choice is in list
                dict_choices[int(choice)]
                break

            # input is not a number
            except ValueError:
                print('Only a number from {} to {}.'.format(
                    list_number[0],
                    list_number[-1]
                ))
            
            # input is not in list
            except KeyError:
                print('Between {} to {}.'.format(
                    list_number[0],
                    list_number[-1]
                ))

        print(
            'User choice : {}. {}'.format(
                choice,
                dict_choices[int(choice)]
            )
        )

        return int(choice) - 1
