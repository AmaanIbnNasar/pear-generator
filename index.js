const fs = require("fs/promises");

async function pairGenerator() {
  const pairs = {};
  const people = shuffleArray(await getPeople());
  let previousWeekPairs = await getPreviousPairs();
  previousWeekPairs = {
    ...previousWeekPairs,
    ...invertObject(previousWeekPairs),
  };
  const paired = new Set();

  for (let j = 0; j < people.length; j++) {
    const personToBePaired = people[j];
    if (paired.has(personToBePaired)) {
      continue;
    }
    for (let i = 0; i < people.length; i++) {
      let possiblePair = people[i];
      const possiblePairIsNotPersonToBePaired =
        possiblePair !== personToBePaired;
      const possiblePairIsNotAlreadyPaired = !paired.has(possiblePair);
      const possiblePairHasBeenPairedBefore =
        previousWeekPairs[personToBePaired] === possiblePair;
      if (
        possiblePairIsNotPersonToBePaired &&
        possiblePairIsNotAlreadyPaired &&
        !possiblePairHasBeenPairedBefore
      ) {
        paired.add(possiblePair);
        paired.add(personToBePaired);
        pairs[personToBePaired] = possiblePair;
        break;
      }
    }
  }
  console.log(Object.keys(pairs).length);
  return people;
}

async function getPeople() {
  const people = await fs.readFile("./__pairfiles__/people.json", "utf-8");
  return JSON.parse(people).people;
}

async function getPreviousPairs() {
  const previousPairs = await fs.readFile(
    "./__pairfiles__/previous_pears.JSON",
    "utf-8"
  );
  return JSON.parse(previousPairs)[0];
}

function invertObject(obj) {
  var new_obj = {};

  for (var prop in obj) {
    if (obj.hasOwnProperty(prop)) {
      new_obj[obj[prop]] = prop;
    }
  }

  return new_obj;
}

function shuffleArray(a) {
  if (a.length === 0) return a;
  var i = a.length,
    t,
    j;
  a = a.slice();
  while (--i)
    (t = a[i]), (a[i] = a[(j = ~~(Math.random() * (i + 1)))]), (a[j] = t);
  return a;
}

module.exports = { pairGenerator, getPeople };

pairGenerator();
