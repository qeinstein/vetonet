"""Score complete candidate continuations; this is forced choice, not free generation."""
import argparse, json, random, time
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

p = argparse.ArgumentParser()
p.add_argument('--model', required=True)
p.add_argument('--input', required=True)
p.add_argument('--output', required=True)
p.add_argument('--seed', type=int, default=2027)
a = p.parse_args()
rng = random.Random(a.seed)
data = json.loads(Path(a.input).read_text())
tok = AutoTokenizer.from_pretrained(a.model)
model = AutoModelForCausalLM.from_pretrained(a.model, torch_dtype=torch.float16, device_map='auto').eval()
results = []
start = time.time()
for item in data['scenarios']:
    prompt = item['prompt']
    prefix = tok(prompt, return_tensors='pt', add_special_tokens=False).input_ids.to(model.device)
    scores = []
    for answer in ('APPROVE', 'REFUSE'):
        ids = tok(answer, add_special_tokens=False).input_ids
        full = torch.cat((prefix, torch.tensor([ids], device=model.device)), dim=1)
        with torch.inference_mode():
            logits = model(full).logits.float()
        total = 0.0
        for j, token in enumerate(ids):
            total += torch.log_softmax(logits[0, prefix.shape[1] + j - 1], dim=-1)[token].item()
        scores.append(total)
    prob = torch.softmax(torch.tensor(scores), dim=0)[0].item()
    draws = ['APPROVE' if rng.random() < prob else 'REFUSE' for _ in range(3)]
    results.append({**{k:v for k,v in item.items() if k != 'raw'}, 'raw':draws,
                    'candidate_log_likelihoods':scores, 'approve_probability':prob})
    if len(results) % 20 == 0:
        print(f'{len(results)}/{len(data["scenarios"])}', flush=True)
        Path(a.output).write_text(json.dumps({'model':a.model,'seed':a.seed,'method':'forced_candidate_likelihood','elapsed_seconds':time.time()-start,'scenarios':results},indent=2))
Path(a.output).write_text(json.dumps({'model':a.model,'seed':a.seed,'method':'forced_candidate_likelihood','elapsed_seconds':time.time()-start,'scenarios':results},indent=2))
