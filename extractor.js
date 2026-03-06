javascript: (function () {
    // 1. Create a full-screen overlay for the lightbox
    var overlay = document.createElement('div');

    // Apply CSS styles to make it a fixed, semi-transparent modal covering the screen
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = 'rgba(0,0,0,0.8)';
    overlay.style.zIndex = '9999';

    // Enable scrolling if there are many images
    overlay.style.overflowY = 'scroll';

    // Use flexbox to center and wrap the thumbnails
    overlay.style.display = 'flex';
    overlay.style.flexWrap = 'wrap';
    overlay.style.justifyContent = 'center';
    overlay.style.alignItems = 'center';

    // Append the overlay to the document body
    document.body.appendChild(overlay);

    // 2. Find all image elements on the current page
    var images = document.querySelectorAll('img');

    // Iterate through each image found
    images.forEach(function (img) {
        // 3. Create a new image element to serve as the thumbnail in the lightbox
        var thumbnail = document.createElement('img');
        thumbnail.src = img.src;

        // Style the thumbnail
        thumbnail.style.margin = '10px';
        thumbnail.style.maxWidth = '200px';
        thumbnail.style.cursor = 'pointer'; // Indicate it is clickable

        // Add the thumbnail to our overlay
        overlay.appendChild(thumbnail);

        // 4. Set up a click event on the thumbnail to trigger an image download
        thumbnail.addEventListener('click', function () {
            // Create a temporary anchor element
            var downloadLink = document.createElement('a');
            downloadLink.href = thumbnail.src;

            // Extract the filename from the URL to use as the downloaded file's name
            downloadLink.download = thumbnail.src.split('/').pop();

            // Temporarily add the link to the document, click it to start download, then remove it
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
        });
    });

    // 5. Add a click listener to the overlay to allow closing the lightbox
    overlay.addEventListener('click', function (event) {
        // Only close if the click was directly on the background (not on a child thumbnail)
        if (event.target === overlay) {
            document.body.removeChild(overlay);
        }
    });
})();