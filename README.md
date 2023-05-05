# poe-stash-filter
Minimal script that creates search regex to highlight items in the stash.

---

The stash in Path of Exile allows RegEx expressions to highlight items that are being searched. 
Upon typing a query in the search bar, the game scans the descriptions of all items in the current stash tab, looking for matches with the query. 
In order to highlight the searched items, the query must contain a unique sequence of characters that matches only the desired properties of an item, and ignores everything else.

Let's assume that we are rolling utility flasks and only want to highlight certain T1 mods. 
To do so, we need to find a unique short text that matches only the desired mod.
For instance, `mad` will only match `of the Armadillo`, which is the T1 %increased armour modifier.

Given a list of all mod descriptions that can appear on a flask, this script will find the shortest regex that matches only the desired mods.

First, we need to load a list of all possible mod descriptions from `data/flask_descriptions`:

```python
with open("data/flask_descriptions") as fh:
  flask_desc = [line.strip() for line in fh.readlines()]
```

Now, we create a list of the desired mods:

```python
highlighted_mods = [
    "Perpetual",  # (46–50)% increased Charge Recovery
    "Flagellant's",  # Gain 3 Charges when you are Hit by an Enemy
    "Alchemist's",  # (23–27)% reduced Duration 25% increased effect
    "of the Armadillo",  # (56–60)% increased Armour during Effect
    "of the Impala",  # (56–60)% increased Evasion Rating during Effect
    "of the Cheetah",  # (12–14)% increased Movement Speed during Effect
    "of the Rainbow",  # (37–40)% additional Elemental Resistances during Effect
    "of the Dove",  # (15–17)% increased Attack Speed during Effect
    "of the Horsefly",  # (15–17)% increased Cast Speed during Effect
    "of Incision",  # (50–55)% increased Critical Strike Chance during Effect
    "of the Owl"  # (60–65)% reduced Effect of Curses on you during Effect
  ]
```

Before we run the script, we will change the descriptions to lowercase because the search is not case-sensitive.

```python
flask_desc = [text.lower() for text in flask_desc]
highlighted_mods = [text.lower() for text in highlighted_mods]
```

Finally, we can print the search RegEx:

```python
from filter_stash import get_search_regex
print(get_search_regex(flask_desc, highlighted_mods))
# prints: ow|ah|tua|sef|pal|nt'|nci|mad|lch|dov
```

You can find this example and the algorithm in `filter_stash.py`.