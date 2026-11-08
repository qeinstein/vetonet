"""Run paired random/no-attack controls across queue-order seeds in one process."""
import runpy,sys
from pathlib import Path
base=Path(__file__).resolve().parent
output=Path(sys.argv[1]); output.mkdir(parents=True,exist_ok=True)
model=sys.argv[2]; inputfile=sys.argv[3]
for seed in range(780,810):
 for name,flag in [('random','--random-attacker'),('control','--no-attack')]:
  sys.argv=[str(base/'model_selected_objections.py'),'--model',model,'--input',inputfile,'--seed',str(seed),flag,'--output',str(output/f'{name}-{seed}.json')]
  runpy.run_path(sys.argv[0],run_name='__main__')
