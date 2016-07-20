sc2skills
=========

sc2skills is a tool for tracking StarCraft 2 ratings. The game includes a
ladder, which tracks your rating (MMR). However, the game only tracks one
rating per player. With sc2skills it is possible to track multiple ratings.

For example, you can compare how well you play with different races. You can
also track the success of individual strategies or play styles that you are
using.


Dependencies
------------

sc2skills requires Python 3.5 or newer.

You also need [trueskill](http://trueskill.org/). It is available in
[PyPi](https://pypi.python.org) or your distribution's package manager.

You can install the dependencies with `pip`:

```bash
$ pip install trueskill
```


Usage
-----

sc2skills uses a text file for loading your match statistics. The file has one
match per line in the following format:

```
<"win"/"loss"> <opponent mmr> <label>
```

The matches must be in chronological order so that most recent games are at the
bottom. `label` can be anything. For example, you can use the race you were
playing or the name of the strategy you used.

For example, `games.txt`:

```
# Comments can be added like this.
loss 3324 oracle_into_blink
win 3522 6_gate_allin
win 3269 6_gate_allin
win 3256 oracle_into_blink
loss 3575 oracle_into_blink
win 3479 6_gate_allin
loss 3520 oracle_into_blink
win 3190 6_gate_allin
win 3505 oracle_into_blink
win 3520 oracle_into_blink
loss 3576 6_gate_allin
loss 3632 6_gate_allin
```

The ratings can be calculated with the following command:

```bash
$ ./main.py <region> <games file>
```

It will show the calculated rating and league for each of your labels along
with the 95% confidence interval.

For example:

```bash
$ ./main.py EU games.txt
6_gate_allin      3604 ± 447 (platinum-2)
oracle_into_blink 3473 ± 393 (gold-1)
```
