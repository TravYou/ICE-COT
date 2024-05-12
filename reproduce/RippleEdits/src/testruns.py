from fact import Fact
from testcase import TestCase
from relation import Relation
from collections import defaultdict
import math

from benchmark import Dataset, Example, TestsAxis
from modeleditor import ROMEModelEditor, InContextModelEditor, MENDModelEditor, MEMITModelEditor
# from queryexecutor import GPT2QueryExecutor, GPT3QueryExecutor, GPTJQueryExecutor, GPTNeoXQueryExecutor, \
    # LlamaQueryExecutor
from testrunner import ExampleResult
from testrunner import TestRunner, TestResult
from in_context_selecter import InContextSelector
import random
import time
if __name__ == "__main__":
    print('started')
    random.seed(2)
    dataset_path = './data/benchmark/popular.json'
    dataset = Dataset.from_file(dataset_path)
    selector = InContextSelector(dataset[:100], selection_method = 'kNN', CoT=True)
    selector.set_icls_embedding([math.inf, math.inf, math.inf, math.inf, math.inf, math.inf])
    selector.set_num_icls(6)
    print(selector.icls)
    start = time.time()
    prompt = 'New Fact: The name of the country which 2021 Myanmar coup d\'état is associated with is duchy of Alsace.\nQuestion: 2021 Myanmar coup d\'état is followed by {answer}.'
    print(selector.get_icls(prompt))
    end = time.time()
    print(f'Run time is {end - start}')
    


