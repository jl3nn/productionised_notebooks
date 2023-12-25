# Use an official Jupyter Notebook base image
FROM jupyter/base-notebook:latest

WORKDIR /app

COPY requirements.txt /app/
COPY dynamic_method_executor.py /app/
COPY magic.py /app/

RUN pip install -r requirements.txt

COPY notebook.ipynb /app/
RUN jupyter nbconvert --to script notebook.ipynb

COPY script_gen.py /app/
COPY workflows.yaml /app/
RUN python script_gen.py

COPY app.py /app/

# Expose the Flask server port
EXPOSE 5001

# Command to run the Flask server
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
