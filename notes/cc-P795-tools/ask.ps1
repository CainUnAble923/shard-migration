$q = @'
P795: the Drover's Handbook is started: the book and Corral work and are tested (Corral: Herding / 8 easier to tame, 25 at 200, for 60 seconds, 5 stamina). You asked to see the numbers for the other three abilities before I build them.

Calm (a wild animal attacking you stops fighting): 3 + Herding / 40 seconds, so 8 seconds at 200. 10 stamina. The same animal cannot be calmed again for 30 seconds. It stops fighting everyone, not only you, as a bard's peacemaking does.

Herd (move a group): every wild animal within 1 + Herding / 40 tiles of the one you target, 6 at 200, up to 1 + Herding / 33 animals, 7 at 200, walks to a spot you pick, up to 10 tiles away. 15 stamina. Each animal rolls on its own as the crook does.

Lure (pull one out of its spawn): one wild animal up to 15 tiles away, in line of sight, walks to you. 10 stamina. 15 is the engine's limit for a herded walk.

For all three: a wild tamable animal only, never a pet, a paragon or a monster; the same chance as the crook (the animal's taming difficulty - 30 to + 30); gains up to the animal's difficulty + 92, so the Dread Warhorse at 108 trains Herding to 200 and a rabbit stops near 91. That + 92 also applies to Corral and is a setting.

Filling the book: Animal Trainers sell the book, with Corral in it, for 2,500 gold, and scrolls to drop in it: Calm 500, Herd 1,000, Lure 1,500. No Herding minimum to buy or use. All numbers are settings.
'@
powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Ask-Chase.ps1 -Question $q `
    -Choice 'Build as drafted|I build Calm, Herd and Lure, the scrolls and the vendor rows with exactly these numbers and finish.' `
    -Choice2 'Stronger|Calm 3 + Herding / 20 (13 seconds at 200), Herd radius 8 and 10 animals at 200, Lure 15 tiles with no line of sight needed; the rest as drafted.' `
    -Choice3 'Weaker|Calm 2 + Herding / 50 (6 seconds at 200), Herd radius 4 and 4 animals at 200, Lure 10 tiles; the rest as drafted.' `
    -Choice4 'Corral only for now|I finish the book with Corral alone, leave the other three pages for a later prompt, and sell no scrolls.'
