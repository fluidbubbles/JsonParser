# **Task**
Given an input as json array (each element is a flat dictionary) write a program that will parse
this json, and return a nested dictionary of dictionaries of arrays, with keys specified in
command line arguments and the leaf values as arrays of flat dictionaries matching appropriate
groups.

Example input for json can be found here: http://jsonformatter.org/74f158.

The output should be something like this: http://jsonformatter.org/615048.

Install requirements

``pip install -r requirements.txt``

### **Run**

In the terminal, navigate to the project folder and run 

##### **CLI**

``python nest.py input.json currency country city``

or

``cat input.json | python nest.py currency country city``

##### **API**


``python app.py``

``curl -d @input.json -X POST http://localhost:5000/parse?keys=currency,city,country -H "Content-Type: application/json" --user admin:admin``


##### **TEST**
In the terminal, navigate to the project folder and run.

``coverage run -m pytest``

