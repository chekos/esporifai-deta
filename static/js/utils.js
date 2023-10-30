function captureAndDownload() {
  const trackDiv = document.getElementById("track");

  html2canvas(trackDiv, { useCORS: true }).then(function (canvas) {  // Removed scale for testing
    const imgData = canvas.toDataURL("image/png");
    const a = document.createElement("a");
    a.href = imgData;
    a.download = "track_image.png";
    a.click();
  });
}
