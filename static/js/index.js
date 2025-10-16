const configs = {
  particles: {
    number: {
      value: 100
    },
    color: {
      value: "#00525c"
    },
    links: {
      enable: true,
      distance: 200,

      color: "#4e99a4"
    },
    shape: {
      type: "circle"
    },
    opacity: {
      value: 1
    },
    size: {
      value: {
        min: 2,
        max: 2
      }
    },
    move: {
      enable: true,
      speed: 2
    }
  },
  background: {
    color: "#fff"
  },
  poisson: {
    enable: true
  },
};


(async (engine) => {
  await loadLinksPreset(engine);

  await engine.load({ id: "tsparticles", options: configs });
})(tsParticles);