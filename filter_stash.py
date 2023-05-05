
class Trie:
  def __init__(self, text=''):
    self.text = text
    self.children = {}

  def add(self, path):
    if not path:
      return
    token = path[0]
    if token in self.children:
      child = self.children[token]
    else:
      child = self.__class__(self.text + token)
      self.children[token] = child
    child.add(path[1:])

  def traverse(self, path):
    node = self
    for token in path:
      if token in node.children:
        child = node.children[token]
        yield child
        node = child
      else:
        raise ValueError('invalid path')

  def traversable(self, path):
    try:
      for _ in self.traverse(path):
        pass
      return True
    except ValueError:
      return False

  def dfs(self):
    for child in self.children.values():
      yield from child.dfs()
    yield self

  def is_leaf(self):
    return len(self.children) == 0


class DataTrie(Trie):
  def __init__(self, text=''):
    super().__init__(text=text)
    self.highlighted = False

  def propagate_highlight_status_(self):
    """Propagate highlighted status from children upwards to the parent.
    Parent is highlighted only if all children all highlighted."""
    if not self.is_leaf():
      self.highlighted = all(
        child.propagate_highlight_status_() for child in self.children.values()
      )
    return self.highlighted


def get_search_regex(texts, highlighted_texts, max_depth=5):
  """Find the shortest search regex to highlight some texts in a corpus."""
  # remove highlighted texts from all texts
  texts = [text for text in texts if text not in highlighted_texts]
  # build trie of texts
  trie = DataTrie()
  for text in texts:
    for i in range(len(text)):
      subtext = text[i:i+max_depth]
      trie.add(subtext)
  # ensure that only the selected texts can be highlighted
  for text in highlighted_texts:
    has_unique_subtext = False
    for i in range(len(text)):
      subtext = text[i:i+max_depth]
      if not trie.traversable(subtext):
        has_unique_subtext = True
        break
    if not has_unique_subtext:
      raise ValueError(f'{text} is not unique, typing it will highlight other texts as well.')
  # add highlighted texts to the trie
  for text in highlighted_texts:
    for i in range(len(text)):
      subtext = text[i:i+max_depth]
      trie.add(subtext)
  # greedily find the shortest sequences that match only the highlighted texts
  regex = []
  while highlighted_texts:
    for node in trie.dfs():
      node.highlighted = True
    # hide texts that should not be highlighted
    for text in texts:
      for i in range(len(text)):
        subtext = text[i:i+max_depth]
        for node in trie.traverse(subtext):
          node.highlighted = False
    # mark nodes that only contain highlighted texts
    trie.propagate_highlight_status_()
    # find the shortest subtext that matches the most highlighted texts
    highlighted_nodes = []
    for node in trie.dfs():
      if node.highlighted:
        matched_texts = [text for text in highlighted_texts if node.text in text]
        score = len(matched_texts) / len(node.text)
        highlighted_nodes.append((score, node.text, matched_texts))
    _, shortest_highlighted_text, matched_texts = max(highlighted_nodes)
    regex.append(shortest_highlighted_text)
    highlighted_texts = [text for text in highlighted_texts if text not in matched_texts]
  return "|".join(regex)


if __name__ == "__main__":
  with open("data/flask_descriptions") as fh:
    flask_desc = [line.strip() for line in fh.readlines()]
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
  flask_desc = [text.lower() for text in flask_desc]
  highlighted_mods = [text.lower() for text in highlighted_mods]
  print(get_search_regex(flask_desc, highlighted_mods))  # ow|ah|tua|sef|pal|nt'|nci|mad|lch|dov
