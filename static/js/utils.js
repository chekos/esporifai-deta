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

function openDivAsImage() {
  const divToCapture = document.getElementById('div-to-capture');
  const canvas = document.createElement('canvas');
  canvas.width = divToCapture.offsetWidth;
  canvas.height = divToCapture.offsetHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(divToCapture, 0, 0, canvas.width, canvas.height);
  const dataURL = canvas.toDataURL('image/png');

  const newWindow = window.open();
  newWindow.document.write(`<img src="${dataURL}"/>`);
}








