const fs = require("fs/promises");

async function pairGenerator() {
  const pairs = [];
  const people = await getPeople();
  const paired = new Set();

  for (let j = 0; j < people.length; j++) {
    const personToBePaired = people[j];
    let pairFound = false;
    if (paired.has(personToBePaired)) {
      continue;
    }
    while (!pairFound) {
      for (let i = 0; i < people.length; i++) {
        let possiblePair = people[i];
        if (possiblePair !== personToBePaired && !paired.has(possiblePair)) {
          paired.add(possiblePair);
          paired.add(personToBePaired);
          pairs.push({ [personToBePaired]: possiblePair });
          pairFound = true;
          break;
        }
      }
    }
  }
  console.log(pairs);
  return people;
}

async function getPeople() {
  const people = await fs.readFile("./__pairfiles__/people.json", "utf-8");
  return JSON.parse(people).people;
}

async function getPreviousPairs() {}

module.exports = { pairGenerator, getPeople };

pairGenerator();
