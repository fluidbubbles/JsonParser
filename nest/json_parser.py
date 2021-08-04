import logging

logging.basicConfig(format='%(message)s')


class JsonParser:
    """ this class parses a json object into dictionary of dictionary of arrays """

    def __init__(self, json_obj, args):
        self.json_obj = json_obj
        self.args = args
        self.leaf = []

    def _get_keys(self, obj):
        """
        finds the values of the keys in json object

        :param obj: A json object
        :return: A list of values of keys of a json obj
        """
        try:
            return [obj[key] for key in self.args]
        except KeyError:
            error_message = 'Key error: Key does not exist in json object'
            logging.error(error_message)
            raise Exception(error_message)

    def _find_leaf(self, obj):
        """
        Strip nesting keys out from the dictionaries in the leaves
        :param obj: A json object
        """
        for index in range(len(self.args)):
            del obj[self.args[index]]
        self.leaf = obj

    def _create_nested_dict(self, keys, dictionary, index=0):
        """
        creates a nested dictionary of dictionaries
        :param keys: Array: An array representing the keys of the nested dictionary
        :param dictionary: dict: A nested dictionary of parsed json object
        :param index: int: An integer which is used to access the next nested key in the keys
        :return: dict: A nested dictionary of parsed json object
        """
        if index >= len(keys):
            return dictionary
        if not dictionary.get(keys[index]) and index == len(keys) - 1:
            dictionary[keys[index]] = [self.leaf]
            return dictionary
        elif index == len(keys) - 1:
            dictionary[keys[index]].append(self.leaf)
        else:
            if dictionary.get(keys[index]) is None:
                dictionary[keys[index]] = {}
            n_dict = dictionary.get(keys[index]) if dictionary.get(keys[index]) else {}
            dictionary[keys[index]] = self._create_nested_dict(keys, n_dict, index + 1)
        return dictionary

    def parse(self):
        """ Parses the json_obj to nested dictionary of arrays
        :return: dict: A nested dictionary of parsed json object
        """
        parsed_json = {}
        if not self.args:
            return self.json_obj
        try:
            for obj in self.json_obj:
                keys = self._get_keys(obj)
                self._find_leaf(obj)
                parsed_json = self._create_nested_dict(keys, parsed_json)
        except TypeError:
            error_message = 'Incorrect input type'
            logging.error(error_message)
            raise Exception(error_message)
        return parsed_json
