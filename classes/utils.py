import json


class Statics():
    """static methos"""

    @staticmethod
    def json_dict(file):
        """Read the parameters from JSON file and convert into dict"""
        with open(file, 'r') as json_file:
            return json.load(json_file)

    @staticmethod
    def input_y_n(msg):
        """User choice between YES or NO"""
        while True:
            choice = input(msg)
            if choice.lower() == "exit":
                exit()
            elif choice.upper() in ('Y', 'YES'):
                choice = True
                break
            elif choice.upper() in ('N', 'NO'):
                choice = False
                break
        return choice

    @staticmethod
    def input_list(list_choices, master=""):
        """Checks if user choice is valid and return choice"""

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
                exit()
            try:
                dict_choices[int(choice)]
                break
            except ValueError:
                print('Only a number from {} to {}.'.format(
                    list_number[0],
                    list_number[-1]
                ))
            except KeyError:
                print('Between {} to {}.'.format(
                    list_number[0],
                    list_number[-1]
                ))

        print('User choice : {}. {}'.format(
            choice,
            dict_choices[int(choice)]
        ))
            
        return int(choice) - 1
