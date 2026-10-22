"""Insert the authored P282 proposal plus generated tables into the F-12 notes."""
from pathlib import Path
import re

root = Path(__file__).parent
text = (root / 'proposal-template.md').read_text(encoding='utf-8')
approved = (root / 'approved-tables.md').read_text(encoding='utf-8')
parts = re.split(r'^## (.+)\n\n', approved, flags=re.MULTILINE)
fragments = dict(zip(parts[1::2], parts[2::2]))
for marker, heading in (('approved-loops', 'Loops'), ('approved-bands', 'Bands'),
                        ('approved-reserves', 'Full reserves'), ('approved-sensitivity', 'Sensitivity')):
    text = text.replace('<!-- P282:' + marker + ' -->', fragments[heading].strip())
comparison = (root / 'tables.md').read_text(encoding='utf-8')
coefficients = comparison.split('## Coefficients\n\n', 1)[1].split('\n\n## Loops', 1)[0]
text = text.replace('<!-- P282:coefficients -->', coefficients.strip())
path = root.parent / 'f12-levels-loops-caps.md'
prefix = path.read_text(encoding='utf-8').split('\n## Proposed numbers, 10-21\n', 1)[0]
path.write_text(prefix + '\n' + text, encoding='utf-8', newline='\n')
print('Assembled F-12 proposal with the approved S2 baseline and labeled alternatives.')
