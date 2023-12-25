import types

class DynamicMethodExecutor:
    def __init__(self, method_order=None):
        self.method_order = method_order or []
        self.method_source_code = {}

    def add_method(self, method_name, code):
        # Add "def" and "return df" to the code
        method_code = f'def {method_name}(self, df):\n{code}\n    return df'

        # Dynamically create a function from the code
        method_func = types.FunctionType(compile(method_code, '<string>', 'exec'), globals(), method_name)

        self.method_source_code[method_name] = method_code

        # Add the function to the instance dictionary
        setattr(self, method_name, method_func)

        # Track the order of added methods
        self.method_order.append(method_name)

    def process(self, df):
        for method_name in self.method_order:
            df = method_name(df)
        return df

    def generate_class_code(self, class_name):
        import_code = f'from dynamic_method_executor import DynamicMethodExecutor\n'
        class_code = f'class {class_name}(DynamicMethodExecutor):\n'
        init_code = f'    def __init__(self):\n        super().__init__('

        # Generate the order of method calls for super()
        method_order = '[' + ', '.join(f'self.{method_name}' for method_name in self.method_order) + ']'
        init_code += f'{method_order})\n'

        code = import_code + class_code + init_code

        # Generate code for each added method
        for method_name in self.method_order:
            method_code = '\n'.join(['    ' + s for s in self.method_source_code[method_name].split('\n')])
            code += f'{method_code}\n'

        return code

    def write_class_code_to_file(self, class_name, file_path):
        class_code = self.generate_class_code(class_name)
        with open(file_path, 'w') as file:
            file.write(class_code)