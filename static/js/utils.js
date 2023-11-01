function captureAndDownload(imageName) {
  const trackDiv = document.getElementById("track");
  const imageSlug = slugify(imageName);
  const scale = 5;
  // Using dom-to-image to capture the element
  domtoimage
    .toPng(trackDiv, {
      width: trackDiv.clientWidth * scale,
      height: trackDiv.clientHeight * scale,
      style: {
        transform: `scale(${scale})`,
        transformOrigin: "top left",
      },
    })
    .then(function (dataUrl) {
      // Create a temporary anchor element to download the image
      const a = document.createElement("a");
      a.href = dataUrl;
      a.download = `${imageSlug}.png`;
      a.click();
    })
    .catch(function (error) {
      console.error("Error capturing image:", error);
    });
}

function generateObjectsWithColor(share) {
  if (share < 1 || share > 100) {
    throw new Error("Share parameter must be between 1 and 100");
  }

  const result = [];

  for (let index = 1; index <= 100; index++) {
    const color = index <= share;
    result.push({ index, color });
  }

  return result;
}

function popularityPlot(popularity) {
  const plot = Plot.plot({
    height: 15,
    x: { domain: [0, 100], label: "", axis: null },
    marks: [
      Plot.tickX(generateObjectsWithColor(popularity), {
        x: "index",
        stroke: "color",
        strokeWidth: 4,
      }),
    ],
  });

  const div = document.querySelector("#popularityPlot");
  div.append(plot);
  console.log(generateObjectsWithColor(20));
}

function slugify(str) {
  return String(str)
    .normalize("NFKD") // split accented characters into their base characters and diacritical marks
    .replace(/[\u0300-\u036f]/g, "") // remove all the accents, which happen to be all in the \u03xx UNICODE block.
    .trim() // trim leading or trailing whitespace
    .toLowerCase() // convert to lowercase
    .replace(/[^a-z0-9 -]/g, "") // remove non-alphanumeric characters
    .replace(/\s+/g, "-") // replace spaces with hyphens
    .replace(/-+/g, "-"); // remove consecutive hyphens
}
