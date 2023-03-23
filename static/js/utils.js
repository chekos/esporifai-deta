function takeScreenshot() {
     html2canvas(document.querySelector("#track")).then(function(canvas) {
        document.body.appendChild(canvas);
      });
   }
