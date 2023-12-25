import yaml
import importlib.machinery
import pandas as pd
import pickle

def execute_preprocessing_workflow(preprocessing_workflow, df):
    for module_name in preprocessing_workflow:
        loader = importlib.machinery.SourceFileLoader(module_name, f"{module_name}_generated.py")
        module = loader.load_module()
        instance = getattr(module, module_name)()
        df = instance.process(df)
    return df

def execute_training_workflow(training_workflow, df):
    model = None
    for module_name in training_workflow:
        loader = importlib.machinery.SourceFileLoader(module_name, f"{module_name}_generated.py")
        module = loader.load_module()
        instance = getattr(module, module_name)()
        model = instance.process(df)  # Assuming the training workflow outputs a model
    return model

def save_model(model, file_path):
    # Replace this with your actual model saving logic
    with open(file_path, 'wb') as file:
        pickle.dump(model, file)

def load_model(file_path):
    # Replace this with your actual model loading logic
    with open(file_path, 'rb') as file:
        model = pickle.load(file)
    return model

def generate_inference_script(preprocessing_workflow, model_file, output_file):
    inference_script = f"""import pandas as pd
import pickle
from script_gen import execute_preprocessing_workflow, load_model

def processing(df):
    # Execute preprocessing workflow
    df = execute_preprocessing_workflow({preprocessing_workflow}, df)

    if 'survived' in df:
        df.drop('survived', axis=1, inplace=True)
    
    # Load pre-trained model from the specified file
    model = load_model("{model_file}")

    # Perform inference
    # Replace this with your actual inference logic using the preprocessed data and model
    inference_result = model.predict(df)
    return inference_result
"""

    with open(output_file, 'w') as script_file:
        script_file.write(inference_script)

def generate_training_script(preprocessing_workflow, training_workflow, model_file, output_file):
    training_script = f"""import pandas as pd
import pickle
from script_gen import execute_preprocessing_workflow, execute_training_workflow, save_model

def processing(df):
    # Execute preprocessing workflow
    df = execute_preprocessing_workflow({preprocessing_workflow}, df)

    # Execute training workflow
    model = execute_training_workflow({training_workflow}, df)

    # Save trained model to the specified file
    save_model(model, "{model_file}")
    return model
"""

    with open(output_file, 'w') as script_file:
        script_file.write(training_script)

if __name__ == "__main__":
    # Example usage:
    yaml_file = 'workflows.yaml'
    with open(yaml_file, 'r') as file:
        workflows = yaml.safe_load(file)

    df = pd.DataFrame()  # Replace with your actual data loading logic

    inference_output = generate_inference_script(workflows['PreProcessing'], workflows['Model'][0], 'inference.py')
    print("inference.py generated")

    training_output = generate_training_script(workflows['PreProcessing'], workflows['Training'], workflows['Model'][0], 'training.py')
    print("training.py generated")