async function takeScreenshot() {
  var trackDiv = document.querySelector("#track");
  var trackContainer = document.querySelector("#track-container");
  html2canvas(trackDiv, { allowTaint: true }).then((canvas) => {
    trackContainer.appendChild(canvas);
  });
}
