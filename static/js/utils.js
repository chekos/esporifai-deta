function captureAndDownload() {
  const trackDiv = document.getElementById("track");

  // Using dom-to-image to capture the element
  domtoimage
    .toPng(trackDiv, {
      width: trackDiv.clientWidth * 2,
      height: trackDiv.clientHeight * 2,
      style: {
        transform: "scale(2)",
        transformOrigin: "top left"
    }})
    .then(function (dataUrl) {
      // Create a temporary anchor element to download the image
      const a = document.createElement("a");
      a.href = dataUrl;
      a.download = "track_image.png";
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
