class Menu:

    """This class is used to create and access a menu in the main program. Menu options are selected by a one character
       entry (longer entries are possible though), and options are shown by printing the menu after options have been
       added to it."""

    # Two dictionaries are created so that options can be looped through and still use normal function names.
    def __init__(self):
        self.option_descriptions = {}
        self.functions = {}

    # Adds an option to the menu. the key is the character the user will need to press to select said option, the
    # description should be a string explanation for what the option does, and the function parameter calls a desired
    # function when the option is selected. The function parameter isn't shown to the user.
    def add_option(self, key, description, function):
        self.option_descriptions[key] = description
        self.functions[key] = function

    # Returns what function should be invoked if one is found. If nothing is found, NoneType is returned.
    def get_choice(self, choice):
        if self.validate_choice(choice):
            return self.functions.get(choice)
        else:
            return 'invalid'

    def validate_choice(self, choice):
        if choice in self.functions.keys():
            return True
        else:
            return False

    # Creates a printable menu with each option on their own line.
    def __str__(self):
        menu_print = ''
        for key in self.option_descriptions.keys():
            menu_print += f'{key}: {self.option_descriptions[key]}\n'
        return menu_print