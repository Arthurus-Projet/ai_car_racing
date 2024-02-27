import pickle

def save_class(file_name, class_instance):
    """
    Save a class instance to a file using pickle.

    Args:
    - file_name (str): The name of the file to save the class instance to.
    - class_instance: The instance of the class to be saved.
    """
    with open(file_name, 'wb') as file:
        pickle.dump(class_instance, file)
    print(f'Class instance saved in {file_name}')

def load_class(file_name):
    """
    Load a class instance from a file using pickle.

    Args:
    - file_name (str): The name of the file containing the saved class instance.

    Returns:
    - object: The loaded class instance.
    """
    try:
        with open(file_name, 'rb') as file:
            loaded_instance = pickle.load(file)
        print(f'Class instance loaded from {file_name}')
        return loaded_instance
    except FileNotFoundError:
        print(f'File {file_name} does not exist. No class instance loaded.')
        return None
