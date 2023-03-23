async function takeScreenshot() {
  window.scrollTo(0, 0);
  var trackDiv = document.querySelector("#track");
  var trackContainer = document.querySelector("#track-container");
  html2canvas(trackDiv, {
    allowTaint: true,
    windowWidth: trackDiv.scrollWidth,
    windowHeight: trackDiv.windowHeight,
    scale: window.devicePixelRatio,
  }).then((canvas) => {
    canvas.id = "track-container-canvas";
    trackContainer.appendChild(canvas);
  });
}
