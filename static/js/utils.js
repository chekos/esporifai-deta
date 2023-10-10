function captureAndDownload() {
  const trackDiv = document.getElementById("track");

  html2canvas(trackDiv, { useCORS: true, scale: 2 }).then(function (canvas) {
    // Convert the canvas to a data URL
    const imgData = canvas.toDataURL("image/png");

    // Create a temporary anchor element to download the image
    const a = document.createElement("a");
    a.href = imgData;
    a.download = "track_image.png";
    a.click();
  });
}
