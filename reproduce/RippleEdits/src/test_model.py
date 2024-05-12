import torch
from sentence_transformers import SentenceTransformer, util
import time
if __name__ == '__main__':
    # tokenizer = AutoTokenizer.from_pretrained('gpt2-medium')
    # tokenizer.pad_token = tokenizer.eos_token
    # model = GPT2LMHeadModel.from_pretrained('gpt2-medium', pad_token_id=tokenizer.eos_token_id).to('cuda')
    # prompt = 'I love fruits.'
    # print(f"The length of prompt is {len(prompt)}")
    # inputs = tokenizer.encode(prompt, return_tensors='pt').to('cuda')
    # print(f"The size of inputs of the prompt is {len(inputs)}")
    prompts =['Male mice exhibit better spatial working and reference memory than females in a water-escape radial arm maze task',
              'I love fruits',
              'The present study examined sex differences in spatial working and reference memory in C57BL/6 mice.\n Males and females were tested in a version of the spatial 8-arm radial arm maze in which the motivating stimulus was escape from water. ',
              'The David Bodian Seminars in Neuroscience are scheduled on Mondays during the academic year, usually at 4 p.m. ET.',
              'See upcoming neuroscience seminars at the Solomon H. Snyder Department of Neuroscience at Johns Hopkins University School of Medicine.',
              'Talks will be in person at the MBI Library (Krieger 341). Some will be recorded for asynchronous viewing. Please contact Chris Fetsch (cfetsch@jhu.edu) to request access to a recorded talk.']
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("model loaded")
    embeddings = model.encode(prompts)
    query = ['What does the agriculture market sell?']
    start = time.time()
    query_embed = model.encode(query)
    hits = util.semantic_search(query_embed, embeddings, score_function=util.dot_score, top_k=2)
    end = time.time()
    print(hits)
    print(f"Time: {end - start}")
    # print(torch.cuda.is_available())  # Should return True if CUDA is properly set up
    # print(torch.cuda.device_count())  # Check how many CUDA devices are available
    # print(torch.cuda.get_device_name(0)) 