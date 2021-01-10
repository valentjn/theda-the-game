#!/usr/bin/python3

import argparse
import os
import random
import sys
from typing import List



def makeUnique(x: List[str]) -> List[str]:
  result = []

  for s in x:
    if s not in result: result.append(s)

  return result



def main() -> None:
  parser = argparse.ArgumentParser(description="Create deck (set of cards) for the game")
  parser.add_argument("--order", type=int, default=5,
      help="Order of the finite projective plane, must be a prime")
  args = parser.parse_args()

  order: int = args.order
  rootDirPath = os.path.abspath(os.path.dirname(__file__))
  symbolsFilePath = os.path.join(rootDirPath, "symbolNames.txt")

  if not os.path.isfile(symbolsFilePath):
    symbolsFilePath = os.path.join(rootDirPath, "symbolNames.template.txt")

  with open(symbolsFilePath, "r") as f: symbols = [x.strip() for x in f.read().split("\n")]
  symbols = [x.replace("\\%", "%") for x in symbols if x != ""]
  random.seed(342)
  random.shuffle(symbols)

  print(f"Creating deck for order n = {order}...")

  finiteSymbols = [symbols[row * order : (row + 1) * order] for row in range(order)]
  infiniteSymbols = symbols[order * order : order * order + order + 1]
  cards = []

  for column0 in range(order):
    for offset in range(order):
      cards.append([finiteSymbols[row][(row * offset + column0) % order] for row in range(order)]
          + [infiniteSymbols[offset]])

  for row in range(order):
    cards.append([finiteSymbols[row][column] for column in range(order)] + [infiniteSymbols[order]])

  cards.append(infiniteSymbols)

  print(f"Checking properties of finite projective plane with order n = {order}...")
  allPropertiesSatisfied = True

  propertySatisfied = ((len(symbols) == order * order + order + 1)
      and (len(makeUnique(symbols)) == order * order + order + 1))
  print(f"Property 1 - there are n^2 + n + 1 symbols: {propertySatisfied}")
  allPropertiesSatisfied &= propertySatisfied

  propertySatisfied = True

  for symbol1 in symbols:
    for symbol2 in symbols:
      if symbol1 == symbol2: continue

      if len([card for card in cards if (symbol1 in card) and (symbol2 in card)]) != 1:
        propertySatisfied = False
        break

  print(f"Property 2 - any two symbols determine a card: {propertySatisfied}")
  allPropertiesSatisfied &= propertySatisfied

  propertySatisfied = True

  for i in range(len(cards)):
    for j in range(len(cards)):
      if i == j: continue

      if len([1 for symbol1 in cards[i] for symbol2 in cards[j] if symbol1 == symbol2]) != 1:
        propertySatisfied = False
        break

  print(f"Property 3 - any two cards share exactly one symbol: {propertySatisfied}")
  allPropertiesSatisfied &= propertySatisfied

  propertySatisfied = all(len([1 for card in cards if symbol in card]) == order + 1
      for symbol in symbols)
  print(f"Property 4 - every symbol is on exactly n + 1 cards: {propertySatisfied}")
  allPropertiesSatisfied &= propertySatisfied

  propertySatisfied = all((len(card) == order + 1) for card in cards)
  print(f"Property 5 - every card contains n + 1 symbols: {propertySatisfied}")
  allPropertiesSatisfied &= propertySatisfied

  if not allPropertiesSatisfied:
    print("Not all properties satisfied; order must be chosen as prime.")
    sys.exit(1)

  print("All properties satisfied.")
  print("")
  print("Deck:")
  print("\n".join("{:>3}.  {}".format(i + 1, ", ".join(random.sample(line, k=len(line))))
      for i, line in enumerate(cards)))



if __name__ == "__main__":
  main()
