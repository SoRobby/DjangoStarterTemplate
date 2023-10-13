let clickCount = 0;  // Counter for the number of clicks on the page

// Event listener to count user clicks
document.addEventListener('click', function () {
    clickCount++;
});


const getOffLoadUserData = () => {
    const offLoadData = {};

    offLoadData.currentTime = new Date().toISOString();

    if (typeof performance !== 'undefined' && typeof performance.timing !== 'undefined') {
        // Page Load Time: The total time taken from initiating the navigation until the document is fully loaded.
        offLoadData.pageLoadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;

        // Time To First Byte (TTFB): Time taken from the user initiating the navigation until the first byte of the
        // response is received. It's a measure of the latency of the server and can include time in queue and other
        // backend delays.
        offLoadData.ttfb = performance.timing.responseStart - performance.timing.navigationStart;

        // DOM Interactive: Time taken from the navigation initiation until the document's DOM is fully constructed, but
        // not necessarily fully loaded (like images).
        offLoadData.domInteractiveTime = performance.timing.domInteractive - performance.timing.navigationStart;

        // DOM Content Loaded: Time taken until the DOMContentLoaded event end. This event is fired when the initial HTML
        // document has been completely loaded and parsed, without waiting for stylesheets, images, and subframes to finish
        // loading.
        offLoadData.domContentLoadedTime = performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart;

        // Redirect Time: If there have been redirects, this captures the time for them.
        offLoadData.redirectTime = performance.timing.redirectEnd - performance.timing.redirectStart;

        // DNS Lookup Time: Time taken to resolve the domain name of the site.
        offLoadData.dnsTime = performance.timing.domainLookupEnd - performance.timing.domainLookupStart;

        // TCP Handshake Time: Time taken to complete the three-way handshake and establish a TCP connection.
        offLoadData.tcpTime = performance.timing.connectEnd - performance.timing.connectStart;

        // Secure Connection Time (HTTPS): If the site is served over HTTPS, this is the time taken to do the TLS handshake.
        offLoadData.tlsTime = performance.timing.secureConnectionStart ? performance.timing.connectEnd - performance.timing.secureConnectionStart : 0;

        // Request Time: Time taken for the server to process the request and send back the response.
        offLoadData.requestTime = performance.timing.responseEnd - performance.timing.requestStart;

        // Response Time: Time taken to read the response/data from the server.
        offLoadData.responseTime = performance.timing.responseEnd - performance.timing.responseStart;

        // Duration the user spent on the page
        offLoadData.duration = Date.now() - performance.timing.navigationStart;
    }

    // Times the user clicked on the page
    offLoadData.clickCount = clickCount;

    return offLoadData;
}

const sendDataToServer = (endpoint, data) => {
    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'X-Custom-Header': 'analytics-beforeunload',
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
}

// Sending data immediately after loading
// sendDataToServer('/analytics/offload-endpoint/', getOffLoadUserData());

// Sending data just before unloading
window.addEventListener('beforeunload', (event) => {
    sendDataToServer('/analytics/beforeunload-endpoint/', {
        // Here you can collect additional data or use the same data
        ...getOffLoadUserData(),
        unloadTime: new Date().toISOString()
    });

    // Prevent default behavior (optional). This can display a warning to the user before leaving the page.
    // event.preventDefault();
    // event.returnValue = '';  // Setting this can show a warning to the user, which may not be desirable.
});



