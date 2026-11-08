$q = @'
P802 (New Haven notes, batch 2) says to build on P799 and to wait if P799 has not merged. P799 is finished but is still in the merge queue (since 11-05 10:47) and has not reached main or the release branch. My P802 branch was cut from main before it, and I am not allowed to merge into my branch, so waiting in this session would not bring P799 in. P802 changes the same lesson files P799 changed, and several of its items depend on P799's places (the theater, the stables, the mine). Nothing of P802 has been started, and nothing is lost by stopping.
'@
powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Ask-Chase.ps1 -Question $q `
    -Choice 'Wait for the merge|I stop now. Once P799 is on main, requeue P802 and a new session cuts its branch from main with P799 in it. This is what the prompt asks for.' `
    -Choice2 'Start on top of P799 now|I merge golem/Iron/P799 into my P802 copy without committing, as P755 did with P743, and go on. If P799 fails its review, P802 needs redoing on top of the fix-up.' `
    -Choice3 'Start only the parts P799 does not touch|I do the Mark and Recall lesson and the audit tables now, and leave the rest until P799 merges. The release diff waits for P799 either way.'
