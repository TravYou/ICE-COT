from fact import Fact
from testcase import TestCase
from relation import Relation
from collections import defaultdict

from benchmark import Dataset, Example, TestsAxis
from modeleditor import ROMEModelEditor, InContextModelEditor, MENDModelEditor, MEMITModelEditor
from queryexecutor import GPT2QueryExecutor, GPT3QueryExecutor, GPTJQueryExecutor, GPTNeoXQueryExecutor, \
    LlamaQueryExecutor
from testrunner import ExampleResult
from testrunner import TestRunner, TestResult
from in_context_selecter import InContextSelector
import random
if __name__ == "__main__":
    print('started')
    random.seed(2)
    dataset_path = './data/benchmark/popular.json'
    dataset = Dataset.from_file(dataset_path)
    selector = InContextSelector(dataset)
    icls_needed = [2, 2, 2, 2, 2, 2]
    selection = selector.select_icls(icls_needed, shuffle = False)
    for sentence in selection:
        print('_____')
        print(sentence)


