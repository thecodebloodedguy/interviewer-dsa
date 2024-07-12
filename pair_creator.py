import json
import re
from dotenv import load_dotenv
import google.generativeai as genai
import os
import time
load_dotenv()
GOOGLE_API_KEY=os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 0,
  "max_output_tokens": 2048,
  "response_mime_type": "application/json",
}

safety_settings = [
{ "category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE",
      "probability": "NEGLIGIBLE" },
    { "category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE",
      "probability": "NEGLIGIBLE" },
    { "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE",
      "probability": "NEGLIGIBLE" },
    { "category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE",
      "probability": "NEGLIGIBLE" },
]

text_model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def convert_to_json(text):
  """Converts a string to JSON, handling potential ``` markers.

  Args:
    text: The string to convert.

  Returns:
    The JSON representation of the string, or None if the conversion fails.
  """

  # Remove ``` markers if present at the beginning and end of the string.
  if text.startswith("`") and text.endswith("`"):
    text = text[3:-3]

  try:
    return json.loads(text)
  except json.JSONDecodeError:
    return None
  
def text_gemini(prompt):
    while True:
        try:
            response = text_model.generate_content(prompt)
            break
        #    print(response.candidate.safety_ratings)
        except Exception as e:
            print(e)
            if e=='429 Resource has been exhausted (e.g. check quota).':
                time.sleep(30)
                continue
    
    return response.text


# Load the data from the JSON file
with open('output_undup.json', 'r') as file:
    data = json.load(file)

def get_latest_version(versions):
    """
    Given a list of versions in string format, this function returns the latest version.
    """
    def version_key(version):
        return [int(v) for v in re.findall(r'\d+', version)]

    return max(versions, key=version_key)

languages_of_interest = ['JavaScript', 'Python', 'C++']
count=0
for element in data:
    start_time = time.time()
    problem_name_var=list(element.keys())[0]
    for problem_name, problem_info in element.items():
        problem_statement = problem_info.get('problem_statement')

        print(f"Problem Name: {problem_name}")

        approach_list=[]
        for approach_name, approach_codes in problem_info.items():
            if approach_name in ['problem_statement', 'difficulty', 'problem_details', 'input_output']:
                continue
            approach_list.append(approach_name)



        for approach_name, approach_codes in problem_info.items():
            if approach_name in ['problem_statement', 'difficulty', 'problem_details', 'input_output']:
                continue
            current_approach=approach_name
            language_versions = {lang: {} for lang in languages_of_interest}
            for language, code in approach_codes.items():
                lang_base = language.split(' ')[0]
                if lang_base in languages_of_interest:
                    language_versions[lang_base][language] = code
                    
            for lang_base, versions in language_versions.items():
                if versions:
                    latest_version = get_latest_version(list(versions.keys()))
                    code_language=latest_version
                    code_text=versions[latest_version]
                    prompt=f'''
                        Given the following input:

                        **Input**:
                        {{
                            "problem": {problem_statement},
                            "answer_provided": {code_text},
                            "code_language": {code_language},
                            "current_approach": {current_approach},
                            "approach_list": {approach_list}'
                        }}

                        Generate a detailed assessment of the provided answer according to the following criteria, comparing it with the available approaches when relevant.

                        **Output format**:
                        {{
                            "overall-rating": "<<rating>>",
                            "correctness": "<<correctness_comment>>",
                            "correctness-rating": "<<correctness_rating>>",
                            "time-complexity": "<<time_complexity_comment>>",
                            "time-complexity-rating': "<<time_complexity_rating>>",
                            "space-complexity": "<<space_complexity_comment>>",
                            "space-complexity-rating": "<<space_complexity_rating>>",
                            "readability": "<<readability_comment>>",
                            "readability-rating": "<<readability_rating>>",
                            "optimization": "<<optimization_comment>>",
                            "optimization-rating": "<<optimization_rating>>",
                            "approach": "<<approach_comment>>",
                            'approach-rating': "<<approach_rating>>",
                            "suggestion": "<<suggestion_comment>>"
                        }}

                        #Please evaluate the provided answer based on the following criteria, comparing it with the approaches in `approach_list`:

                        **Correctness**:
                        1. **Functional Correctness**: Verify if the code produces the correct output for a wide range of test cases, including edge cases. Ensure that all specified problem requirements are met.
                        2. **Boundary Condition Handling**: Test the code against boundary conditions such as minimum and maximum input sizes, empty inputs, and extreme values. Ensure that the code gracefully handles these conditions without errors or unexpected behavior.
                        3. **Exception and Error Handling**: Evaluate the robustness of the code in handling runtime errors, exceptions, and invalid inputs. Ensure that appropriate error messages or handling mechanisms are in place.
                        4. **Logic and Flow Consistency**: Analyze the logical flow of the code to ensure it is consistent and free from logical errors. Check for off-by-one errors, infinite loops, and other common pitfalls.
                        5. **Comprehensive Testing**: Ensure that the code is accompanied by a comprehensive set of unit tests and integration tests. Verify that the tests cover all possible scenarios, including normal cases, edge cases, and error conditions.

                        **Optimization**:
                        1. **Time Complexity Improvement**: Assess the reduction in time complexity due to the optimization. Compare the pre- and post-optimization time complexity and measure the practical performance gains.
                        2. **Space Complexity Improvement**: Evaluate the reduction in space complexity. Analyze memory usage before and after optimization and consider if space is being used efficiently.
                        3. **Algorithmic Enhancements**: Identify specific techniques or optimizations used (e.g., memoization, pruning, lazy evaluation). Assess the impact of these techniques on overall performance.
                        4. **Code Refactoring and Simplification**: Determine if the optimization has simplified the codebase without compromising readability. Ensure that refactored code maintains or improves clarity and maintainability.
                        5. **Benchmarking and Profiling**: Use benchmarking tools to measure performance improvements quantitatively. Profile the code to identify bottlenecks and verify that optimizations address these areas effectively.

                        **Approach**:
                        1. **Algorithmic Efficiency**: Evaluate the time complexity in Big-O notation and whether it is optimal for the given problem. Compare with standard algorithms and assess if the chosen approach minimizes the number of operations.
                        2. **Data Structure Utilization**: Check if appropriate data structures are used to achieve optimal performance (e.g., stacks, queues, hashmaps). Assess if the data structures chosen are necessary and efficiently utilized.
                        3. **Algorithm Design**: Analyze the algorithm's design pattern (e.g., divide-and-conquer, dynamic programming, greedy) and its suitability for the problem. Consider the clarity of the algorithm's logic and flow.
                        4. **Scalability and Extensibility**: Determine if the algorithm can handle large inputs without significant performance degradation. Evaluate if the approach can be easily extended or modified to accommodate additional requirements.
                        5. **Correctness Proof**: Validate the correctness of the algorithm through formal proofs or logical reasoning. Ensure that the algorithm adheres to the problem constraints and expected behavior.

                        **Example Input**:
                        {{
                            "problem": "Find the next greater element for each element in an array",
                            "answer_provided": "def nextGreaterElement(arr):\n    n = len(arr)\n    next_greater = [-1] * n\n    stack = []\n    for i in range(n-1, -1, -1):\n        while stack and stack[-1] <= arr[i]:\n            stack.pop()\n        if stack:\n            next_greater[i] = stack[-1]\n        stack.append(arr[i])\n    return next_greater",
                            "code_language": "Python",
                            "current_approach": "Using Stack",
                            "approach_list": ['Brute Force', 'Using Stack' , 'Optimal Approach']
                        }}

                        **Example Output**:
                        {{
                            "overall-rating": "4",
                            "correctness": "The code correctly finds the next greater element for each element in the array for most test cases, but fails for some edge cases.",
                            "correctness-rating": "4",
                            "time-complexity": "The time complexity is O(n), which is optimal for this problem.",
                            "time-complexity-rating": "5",
                            "space-complexity": "The space complexity is O(n) due to the stack and result array.",
                            "space-complexity-rating": "4",
                            "readability": "The code is readable with clear variable names, but lacks comments.",
                            "readability-rating": "3",
                            "optimization": "No further optimizations are necessary as the code is already optimal.",
                            "optimization-rating": "5",
                            "approach": "The approach using a stack is efficient and appropriate for the problem. Compared to the brute force approach, this is much more efficient. The optimal approach, however, could offer slightly better performance in certain cases.",
                            "approach-rating": "4",
                            "suggestion": "Add comments and handle more edge cases to improve correctness."
                        }}

                        '''
                    completion=text_gemini(prompt)
                    prompt=f'''{{"problem": {problem_statement},"answer_provided": {code_text},"code_language": {code_language},}}'''
                    count+=1
                    if count==1400:
                        print(f'was doin for {problem_name_var}')
                        print('Credit Ended')
                        time.sleep(1000)
                    completion=convert_to_json(completion)
                    # prompt=convert_to_json(prompt)
                    try:
                        with open('pairs.jsonl' , 'a') as file:
                            jsonl_entry = {"prompt": "Evaluate the following DSA solution:"+prompt, "completion": json.dumps(completion)}
                            file.write(json.dumps(jsonl_entry) + "\n")
                    except Exception as e:
                        with open('pairs.txt', 'a') as file:
                            file.write(e)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")

        
    print(f'Done for {problem_name_var}')