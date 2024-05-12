import json
from transformers import AutoModelForCausalLM, AutoTokenizer

with open('datasets/MQuAKE-CF-3k.json', 'r') as f:
    dataset = json.load(f)


all_knowledge = []

i = 0 


for entry in dataset:
    thoughts = []

  
    for rewrite in entry["requested_rewrite"]:
        new_fact = {
            "new_fact": f'{rewrite["prompt"].format(rewrite["subject"])} {rewrite["target_new"]["str"]}',
        }
        all_knowledge.append(new_fact)
   
    questions = entry['questions']
    first_question = questions[0]
    answer = entry['new_answer']
        
    for hop in entry["new_single_hops"]:
        thought = f"{hop['cloze']} {hop['answer']}."
        thoughts.append(thought)

    
    if thoughts:  
        combined_thoughts = " ".join(thoughts)
        knowledge_entry = {
            "Questions": first_question,
            "Thoughts": combined_thoughts,
            "Answer": answer,
            
        }
        all_knowledge.append(knowledge_entry)

    


print("New Knowledge Examples:")
for nk in all_knowledge[:5]:  
    print(nk)
    
    



model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-j-6B")
tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")

prompt = (
    "In a shocking finding, scientists discovered a herd of unicorns living in a remote, "
    "previously unexplored valley, in the Andes Mountains. Even more surprising to the "
    "researchers was the fact that the unicorns spoke perfect English."
)

input_ids = tokenizer(prompt, return_tensors="pt").input_ids

gen_tokens = model.generate(
    input_ids,
    do_sample=True,
    temperature=0.9,
    max_length=100,
)
gen_text = tokenizer.batch_decode(gen_tokens)[0]

