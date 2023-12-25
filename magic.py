from dynamic_method_executor import DynamicMethodExecutor
from IPython.core.magic import (register_cell_magic)
from IPython import get_ipython


@register_cell_magic
def add_to(line, cell):
    parts = line.split()
    class_name = parts[0].strip()
    method_name = parts[1].strip()
    code = cell.strip()
    indented_code = '\n'.join(['    ' + line for line in code.split('\n')])

    # Dynamically create an instance of the class if it doesn't exist
    if class_name not in globals():
        print(f"Creating instance of class {class_name}")
        instance = DynamicMethodExecutor()
        globals()[class_name] = instance
    else:
        instance = globals()[class_name]

    # Add method to the instance
    instance.add_method(method_name, indented_code)
    get_ipython().run_cell(cell)

@register_cell_magic
def export_all(line, cell):
    for class_name, class_obj in globals().items():
        if isinstance(class_obj, DynamicMethodExecutor) and class_name != "DynamicMethodExecutor":
            file_path = f"{class_name}_generated.py"
            class_obj.write_class_code_to_file(class_name, file_path)
