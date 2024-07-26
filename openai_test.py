from openai import OpenAI

import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Retrieve the API key from the environment variable
api_key = os.getenv('OPEN_AI_KEY')

OPEN_AI_KEY=api_key

client = OpenAI(
    # This is the default and can be omitted
    api_key=OPEN_AI_KEY
)

def text_gemini(prompt,model):
   completion = client.chat.completions.create(
  model=model,
  messages=[
    {"role": "system", "content": "You evaluate DSA problems and return a json format output."},
    {"role": "user", "content": prompt}
  ]
)
   return extract_json(completion.choices[0].message.content)

# print(completion.choices[0].message)
import re

def extract_json(text):
    # Regular expression pattern to match text between ```json and ```
    json_block_pattern = re.compile(r'```json(.*?)```', re.DOTALL)
    
    # Search for the JSON block pattern in the input text
    match = json_block_pattern.search(text)
    
    if match:
        return match.group(1).strip()  # Return the matched JSON block, stripped of leading/trailing whitespace
    else:
        return text




def fet_ratin(problem,solution,testcase=None,typ=None):
   if typ=='standard-test-case':
      prompt=f'''
Evaluate the solution for DSA problem for given testcases.
Problem:{problem}
Test-Cases:{testcase}
Solution:{solution}

### Try to analyze all standard test cases to find out rating
### avoid considering time complexity, space complexity or any optimization while rating
### keep rating-reason to a single line

Now consider all knowledge you have regarding this problem and solution it haves, thoroughly inspect the code for all test cases and find out rating as per criteria below:
  - -1 if solution is not a code , un implementable code, un necessary text
  - 0 if solution does not solve the problem.
  - 1 if Attempted but incorrect.
  - 2 if solution Solves part of the problem.
  - 3 if Solution solves the problem but inefficiently or with minor deflections in result.
  - 4 if solution correctly solves the problem but misses edge cases.
  - 5 if solution perfectly solves the problem.

## Avoid extra texts and explainations and bold texts,new lines
##every string in output is single lined.

output format:
 {{"rating":integer(rating),"rating-description":string(rating-description),"rating-reason":string(rating-reason)}}

'''
   if typ=='bug-free-case':
      prompt=f'''
Evaluate the solution for DSA problem for bugs.
Problem:{problem}
Solution:{solution}

output format:
 {{"rating":integer(rating),"rating-description":string(rating-description),"rating-reason":string(rating-reason)}}

      '''
   if typ=='edge-cases':
      prompt=f'''
Evaluate the solution for DSA problem for given testcases.
Problem:{problem}
Test-Cases:{testcase}
Solution:{solution}

### Compare with similar solutions for this problem that fails at negative or edge cases 
### avoid considering time complexity, space complexity or any optimization while rating
### keep rating-reason to a single line


Now consider all knowledge you have regarding this problem and solution it haves, thoroughly inspect the code find out rating as per criteria below:
  - -1 if solution is not a code , un implementable code, un necessary text
  - 0: The solution does not consider edge cases at all.
  - 2: The solution attempts to handle edge cases but does so incorrectly.
  - 4: The solution handles some edge cases but misses others.
  - 5: The solution perfectly handles all edge cases.

## Avoid extra texts and explainations and bold texts,new lines
##every string in output is single lined.

output format:
 {{"rating":integer(rating),"rating-description":string(rating-description),"rating-reason":string(rating-reason)}}

'''
   if typ=='time-complexity': 
      prompt=f'''
Evaluate the solution for DSA problem for time complexity.
Problem:{problem}
Solution:{solution}

### Find the time complexity of the solution and compare it with time complexities of solution for this problem .
### keep rating-reason to a single line


**Instruction**: If a function is used inside the main executable , make sure to consider it in calculating complexity.Also use seperate techniques for recursive approaches.
Rate the solution's time complexity on basis of the below guidelines:
  - -1 if solution is not a code , un implementable code, un necessary text
  - 1 if EXCEPTIONALLY HIGH time that might be too much for computation.
  - 3 if complexity is very much higher than the best possible time complexity for given problem.
  - 4 if complexity nearer to best possible complexity but not as good.
  - 5 if best possible time complexity for provided problem.
## Avoid extra texts and explainations and bold texts,new lines
##every string in output is single lined.

output format:
 {{"rating":integer(rating),"rating-description":string(rating-description),"rating-reason":string(rating-reason)}}

'''
   if typ=='space-complexity':
      prompt=f'''
Evaluate the solution for DSA problem for space complexity.
Problem:{problem}
Solution:{solution}

### Find the space complexity of the solution and compare it with space complexities of solution for this problem.
### keep rating-reason to a single line


**Instruction**:To calculate space complexity, consider number of variables, their structures such as array,trees etc. Use standard methods to estimate space complexity
## Avoid time complexity and only look after space complexity.
Rate the solution's space complexity on basis of the below guidelines:
  - -1 if solution is not a code , un implementable code, un necessary text
  - 1 if EXCEPTIONALLY HIGH space that is too much for computation.
  - 3 if complexity is very much higher than the best possible space complexity for given problem.
  - 4 if complexity nearer to best possible complexity but not as good.
  - 5 if best possible space complexity for provided problem.
## Avoid extra texts and explainations and bold texts,new lines
##every string in output is single lined.

output format:
 {{"rating":integer(rating),"rating-description":string(rating-description),"rating-reason":string(rating-reason)}}

'''
   if typ=='algorithm ':
      prompt=f'''
Evaluate the solution for DSA problem for Algorithm used in it.
Problem:{problem}
Solution:{solution}

### Find the algorithm used in the solution and compare the algorithm used in the solution with other algorithm that can be used for this 
### Brute force approaches are usually worse than optimized one
### avoid considering time complexity, space complexity or any optimization while rating
### keep rating-reason to a single line


Make sure you find proper approach. Avoid hallucinating new approaches by yourself
Rate the solution on basis of the below guidelines:
  - -1 if solution is not a code , un implementable code, un necessary text
  - 0 if No clear algorithm or incorrect algorithm used.
  - 1 if Attempted an algorithm but incorrect.
  - 2 if Partially correct algorithm but incomplete.
  - 3 if Correct algorithm but incorrect implementation.
  - 4 if Correct and optimal algorithm with minor improvements needed.
  - 5 if Excellent algorithm choice and implementation.
## Avoid extra texts and explainations and bold texts,new lines
##every string in output is single lined.

output format:
 {{"rating":integer(rating),"rating-description":string(rating-description),"rating-reason":string(rating-reason)}}

'''
   if typ=='saclability-extensibility':
      prompt=f'''
Evaluate the solution for DSA problem for Scalability and Extensibility.
Problem:{problem}
Solution:{solution}

### Compare the solution with scalable and extensible solutions for similar problems to find out the rating
### keep rating-reason to a single line


Rate the solution on basis of the below guidelines:
  - -1 if solution is not a code , un implementable code, un necessary text
  - 0 if in correct code.
  - 1 if very high time and space complexity.
  - 3 if moderate time and space complexity and some edge cases left.
  - 5 if optimal scalable and well written code solving all edge cases.
## Avoid extra texts and explainations and bold texts,new lines
## every string in output is single lined.

output format:
 {{"rating":integer(rating),"rating-description":string(rating-description),"rating-reason":string(rating-reason)}}

'''
   if typ=='dsa-utilization':
      
      prompt=f'''
Evaluate the solution for DSA problem for Data Structure Utilization.
Problem:{problem}
Solution:{solution}

### Find out the data structure used in the solution and compare it with solution of similar problem to compare usage of data structures
### avoid considering time complexity, space complexity or any optimization while rating
### keep rating-reason to a single line

Rate the solution on basis of the below guidelines:
  - -1 if solution is not a code , un implementable code, un necessary text
  - 0 if No data structure used at all.
  - 1 if Attempted but incorrect data structure.
  - 2 if Partially correct data structure but not fully utilized.
  - 3 if Correct data structure but incorrect implementation.
  - 4 if Correct use of data structure with minor improvements needed.
  - 5 if Excellent choice and use of data structures.
## Avoid extra texts and explainations and bold texts,new lines
##every string in output is single lined.
output format:
 {{"rating":integer(rating),"rating-description":string(rating-description),"rating-reason":string(rating-reason)}}

'''
   return text_gemini(prompt)

def all_ratin(problem,solution,testcase):
   rat={}
   desc={}
   rex=''
   for i in ['standard-test-case','bug-free-case','edge-cases','time-complexity','space-complexity','algorithm ','saclability-extensibility','dsa-utilization']:
      tex=fet_ratin(problem,solution,testcase,i)
      print(tex)
      print(type(tex))
      # tex=json.loads(tex)
      desc[i]=tex
      # rex=rex+tex+'\n\n\n\n\n\n'
      rat[i]=json.loads(tex)['rating']
      
   return rat,desc



app = Flask(__name__)
CORS(app)


@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    problem = data.get('problem')
    solution = data.get('solution')
    testcase = data.get('testcase', None)

    if not problem or not solution:
        return jsonify({"error": "Problem and solution fields are required"}), 400
    
    try:
       ratings,desc= all_ratin(problem, solution, testcase)
       final = {}
       final['correctness'] = round(ratings['standard-test-case'] * 0.3333 + ratings['bug-free-case'] * 0.3333 + ratings['edge-cases'] * 0.3333)
       final['optimization'] = round(ratings['time-complexity'] * 0.66666 + ratings['space-complexity'] * 0.3333)
       final['approach'] = round(ratings['algorithm '] * 0.6 + ratings['saclability-extensibility'] * 0.2 + ratings['dsa-utilization'] * 0.2)
       final['over-all'] = round(final['correctness'] * 0.45 + final['optimization'] * 0.3 + final['approach'] * 0.25)
       desc={key: json.loads(value) for key, value in desc.items()}
       desc['ratings']=final
       new=desc
    except Exception as e:
       print('Error:',e)
       new={"mess":"retry-failed due to api errors" , "error" : e}

    data_to_save = {
        'problem': problem,
        'solution': solution,
        'testcase': testcase,
        'result':new
    }
    with open('results.json', 'a') as file:
      json.dump(data_to_save,file)
      file.write(',')

    return jsonify(new)

@app.route('/evaluatex', methods=['POST'])
def evaluate():
    data = request.json
    problem = data.get('problem')
    solution = data.get('solution')
    testcase = data.get('testcase', None)
    model = data.get('model', 'gpt-3.5-turbo')  # Default to 'gpt-3.5-turbo' if not provided

    if not problem or not solution:
        return jsonify({"error": "Problem and solution fields are required"}), 400
    
    try:
        def text_gemini(prompt, model):
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You evaluate DSA problems and return a json format output."},
                    {"role": "user", "content": prompt}
                ]
            )
            return extract_json(completion.choices[0].message.content)

        ratings, desc = all_ratin(problem, solution, testcase)
        final = {}
        final['correctness'] = round(ratings['standard-test-case'] * 0.3333 + ratings['bug-free-case'] * 0.3333 + ratings['edge-cases'] * 0.3333)
        final['optimization'] = round(ratings['time-complexity'] * 0.66666 + ratings['space-complexity'] * 0.3333)
        final['approach'] = round(ratings['algorithm '] * 0.6 + ratings['saclability-extensibility'] * 0.2 + ratings['dsa-utilization'] * 0.2)
        final['over-all'] = round(final['correctness'] * 0.45 + final['optimization'] * 0.3 + final['approach'] * 0.25)
        desc = {key: json.loads(value) for key, value in desc.items()}
        desc['ratings'] = final
        new = desc
    except Exception as e:
        print('Error:', e)
        new = {"mess": "retry-failed due to api errors", "error": str(e)}

    data_to_save = {
        'problem': problem,
        'solution': solution,
        'testcase': testcase,
        'result': new
    }
    with open('resultsx.json', 'a') as file:
        json.dump(data_to_save, file)
        file.write(',')

    return jsonify(new)



if __name__ == '__main__':
    app.run(debug=True)