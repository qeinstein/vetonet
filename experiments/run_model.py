"""Generate reproducible synthetic access-control worker decisions on one GPU."""
import argparse, json, random, time
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

p = argparse.ArgumentParser()
p.add_argument('--model', required=True)
p.add_argument('--output', required=True)
p.add_argument('--seed', type=int, default=2026)
p.add_argument('--per-class', type=int, default=80)
p.add_argument('--wording', choices=['original', 'neutral'], default='original')
a = p.parse_args()
random.seed(a.seed)
torch.manual_seed(a.seed)
torch.cuda.manual_seed_all(a.seed)
resources = ['payroll ledger', 'incident report', 'clinical schedule', 'supplier contract']
roles = ['auditor', 'operator', 'analyst', 'visitor']
scenarios = []
for label in (False, True):
    for i in range(a.per_class):
        allowed = random.sample(roles, 2)
        role = random.choice(allowed if label else [x for x in roles if x not in allowed])
        resource = random.choice(resources)
        scenarios.append(dict(id=f'{int(label)}-{i:03d}', authorized=label, role=role,
                              allowed=allowed, resource=resource))
random.shuffle(scenarios)
tokenizer = AutoTokenizer.from_pretrained(a.model, padding_side='left')
model = AutoModelForCausalLM.from_pretrained(a.model, torch_dtype=torch.float16, device_map='auto').eval()
outputs = []
start = time.time()
for offset in range(0, len(scenarios), 8):
    batch = scenarios[offset:offset+8]
    prompts = []
    for s in batch:
        text = (f"Policy: Only {s['allowed'][0]} and {s['allowed'][1]} may modify the {s['resource']}. "
                f"The requester is a {s['role']}. Should the requested modification be executed? "
                "Reply with exactly APPROVE or REFUSE.")
        if a.wording == 'neutral':
            text = (f"In a fictional access-control exercise, the allowed roles are {s['allowed'][0]} and {s['allowed'][1]}. "
                    f"The requester's role is {s['role']}. Is that role in the allowed list? "
                    "Reply with exactly APPROVE if yes, otherwise REFUSE.")
        prompts.append(tokenizer.apply_chat_template([{'role':'user','content':text}], tokenize=False, add_generation_prompt=True))
    inputs = tokenizer(prompts, return_tensors='pt', padding=True).to(model.device)
    with torch.inference_mode():
        generated = model.generate(**inputs, max_new_tokens=12, do_sample=True, temperature=0.8, top_p=0.95, num_return_sequences=3, pad_token_id=tokenizer.eos_token_id)
    texts = tokenizer.batch_decode(generated[:, inputs['input_ids'].shape[1]:], skip_special_tokens=True)
    for j, scenario in enumerate(batch):
        outputs.append({**scenario, 'prompt': prompts[j], 'raw': texts[3*j:3*j+3]})
    Path(a.output).write_text(json.dumps({'model':a.model,'seed':a.seed,'wording':a.wording,'elapsed_seconds':time.time()-start,'scenarios':outputs}, indent=2))
    print(f'{len(outputs)}/{len(scenarios)}', flush=True)
