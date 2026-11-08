"""Create a LaTeX/PGFPlots figure from stored synthetic queue results."""
import json
from pathlib import Path
rows=json.loads(Path('results/hidden_flood_allocations.json').read_text())['results']
styles={'dedup_fifo':'blue','dedup_risk':'red','dedup_evidence':'black'}
labels={'dedup_fifo':'FIFO + dedup','dedup_risk':'Risk + dedup','dedup_evidence':'Evidence-aware'}
parts=[r'\begin{tikzpicture}',r'\begin{groupplot}[group style={group size=2 by 1,horizontal sep=1.2cm},width=0.48\textwidth,height=4.3cm,xlabel={Verification budget},xmin=25,xmax=125,xtick={30,60,120},ymin=0,ymax=0.65,legend style={font=\scriptsize},tick label style={font=\scriptsize},label style={font=\scriptsize},title style={font=\scriptsize}]']
for attack in (0,3):
 parts.append(r'\nextgroupplot[title={'+('No injected objections' if attack==0 else 'Three injected objections')+r'},ylabel={Authorized completion}]')
 for strategy,color in styles.items():
  subset=sorted((r for r in rows if 'qwen' in r['dataset'] and r['strategy']==strategy and r['extra_per_attacked_case']==attack),key=lambda r:r['budget'])
  assert len(subset)==3
  coords=' '.join(f"({x['budget']},{x['completion'][0]:.5f})" for x in subset)
  parts.append(r'\addplot+[mark=*,color='+color+'] coordinates {'+coords+'};')
  if attack==0:parts.append(r'\addlegendentry{'+labels[strategy]+'}')
parts += [r'\end{groupplot}',r'\end{tikzpicture}']
Path('images/budget_figure.tex').write_text('\n'.join(parts)+'\n')
