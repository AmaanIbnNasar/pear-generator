const { pairGenerator, getPeople } = require("../index");

describe("Pair Generator", () => {
  it("Return a promise", () => {
    expect(typeof pairGenerator()).toEqual("object");
  });
  it("Return an array of pairs", (done) => {
    pairGenerator().then((data) => {
      expect(typeof data).toEqual("object");
      done();
    });
  });
});
