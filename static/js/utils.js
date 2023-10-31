function captureAndDownload() {
    const trackDiv = document.getElementById("track");

    // Using dom-to-image to capture the element
    domtoimage.toPng(trackDiv)
        .then(function (dataUrl) {
            // Create a temporary anchor element to download the image
            const a = document.createElement("a");
            a.href = dataUrl;
            a.download = "track_image.png";
            a.click();
        })
        .catch(function (error) {
            console.error('Error capturing image:', error);
        });
}
