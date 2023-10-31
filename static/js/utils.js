function captureAndAppend() {
    const trackDiv = document.getElementById("track");

    // Using dom-to-image to capture the element
    domtoimage.toPng(trackDiv)
        .then(function (dataUrl) {
            // Create an img element
            const img = new Image();
            img.src = dataUrl;

            // Append the img to a container, for example, to the body or another div
            const container = document.getElementById("track");
            container.appendChild(img);
        })
        .catch(function (error) {
            console.error('Error capturing image:', error);
        });
}
