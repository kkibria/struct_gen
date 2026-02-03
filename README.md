manages skeliton based lyric maintenece


It need project toml file called `struct.toml` at the project root.
a sample `struct.toml` file,

```toml
[song_pat]

ivvpcbo = "ivpcvpcbco"

[translate]

tts = """
~ = \\n 
| = \\n 
. =
, =
; =
- =
শুভ = শুভো
কামনায় = কামোনায
মানবতায় = মানোবতায়
শক্তি = শোক্তি
চির = চিরো
দানে = দানেএ
ফসল = ফশোল
জ্ঞান = গ্যান
মায়ার = মায়আর
তোকে = তোকেএ
"""

unpub = """
~ =
| = \\n 
"""

subtitle = """
~ =
| = 
. =
, =
; =
"""

[tag]
subtitle = false




