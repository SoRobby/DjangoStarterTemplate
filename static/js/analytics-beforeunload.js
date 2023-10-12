let clickCount = 0;  // Counter for the number of clicks on the page

// Event listener to count user clicks
document.addEventListener('click', function () {
    clickCount++;
});


const getOffLoadUserData = () => {
    const offLoadData = {};

    offLoadData.currentTime = new Date().toISOString();
    offLoadData.userAgent = navigator.userAgent;
    offLoadData.window = {
        width: window.innerWidth,
        height: window.innerHeight,
    }
    offLoadData.preferredLanguage = navigator.language;
    offLoadData.platform = navigator.platform;
    offLoadData.referrer = document.referrer;

    // Page Load Time
    offLoadData.pageLoadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;

    // Duration the user spent on the page
    offLoadData.duration_ms = Date.now() - performance.timing.navigationStart;

    // Times the user clicked on the page
    offLoadData.clickCount = clickCount;

    // Determine if user is likely a bot based on the user agent string
    // Note: This is a simplistic method and may not catch all bots
    const botPatterns = [
        /bot/, /crawl/, /spider/, /slurp/, /search/, /archiver/, /archive/, /wget/, /curl/, /linkchecker/
    ];
    offLoadData.isLikelyBot = botPatterns.some(pattern => pattern.test(offLoadData.userAgent.toLowerCase()));


    return offLoadData;
}

const sendDataToServer = (endpoint, data) => {
    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'X-Custom-Header': 'Analytics',
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


// const gatherUserData = () => {
//             const userData = {};
//
//             // Browser and System Information
//             userData.userAgent = navigator.userAgent;
//             userData.platform = navigator.platform;
//             userData.cpuCores = navigator.hardwareConcurrency;
//
//             // Screen & Window Information
//             userData.screenResolution = {
//                 width: screen.width,
//                 height: screen.height,
//             };
//             userData.windowSize = {
//                 width: window.innerWidth,
//                 height: window.innerHeight,
//             };
//             userData.availableScreenSize = {
//                 width: screen.availWidth,
//                 height: screen.availHeight,
//             };
//             userData.colorDepth = screen.colorDepth;
//             userData.pixelDepth = screen.pixelDepth;
//
//             // Location Data
//             userData.referrerURL = document.referrer;
//
//             // Note: Geolocation often prompts the user for permission
//             if ('geolocation' in navigator) {
//                 navigator.geolocation.getCurrentPosition(position => {
//                     userData.location = {
//                         latitude: position.coords.latitude,
//                         longitude: position.coords.longitude,
//                     };
//                 });
//             }
//
//             // Connection Information (may not be available on all browsers)
//             if (navigator.connection) {
//                 userData.networkInfo = {
//                     type: navigator.connection.effectiveType,
//                     downlink: navigator.connection.downlink,
//                     rtt: navigator.connection.rtt,
//                 };
//             }
//
//             // Device Capabilities & Features
//             userData.touchSupported = 'ontouchstart' in window;
//             userData.isOnline = navigator.onLine;
//             userData.preferredLanguage = navigator.language || navigator.userLanguage;
//             {#userData.timezoneOffset = new Date().getTimezoneOffset();#}
//
//             // Browser Preferences
//             userData.doNotTrack = navigator.doNotTrack === "1" ? true : false;
//             if (window.matchMedia && window.matchMedia('(prefers-color-scheme)').matches) {
//                 userData.colorSchemePreference = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
//             }
//
//             // Page Load Time # TODO - need to fix, not working properly
//             userData.pageLoadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
//
//
//             // User Clicks
//             userData.clickCount = 0;
//             document.addEventListener('click', function () {
//                 userData.clickCount++;
//             });
//
//
//             // Time Spent on Page
//             userData.pageEnterTime = Date.now();
//             window.addEventListener('beforeunload', function () {
//                 userData.timeSpentOnPage = Date.now() - userData.pageEnterTime;
//
//                 // Here, you might want to send this data to your server, because the user is leaving the page
//             });
//
//
//             // Cookies & Storage
//             // Note: This will only get the size of storage items, not their content.
//             userData.localStorageSize = Object.keys(localStorage).length;
//             userData.sessionStorageSize = Object.keys(sessionStorage).length;
//
//             // Device Orientation & Motion
//             if ('DeviceOrientationEvent' in window) {
//                 window.addEventListener('deviceorientation', event => {
//                     userData.deviceOrientation = {
//                         alpha: event.alpha,
//                         beta: event.beta,
//                         gamma: event.gamma,
//                     };
//                 });
//             }
//             if ('DeviceMotionEvent' in window) {
//                 window.addEventListener('devicemotion', event => {
//                     userData.deviceMotion = {
//                         acceleration: event.acceleration,
//                         accelerationIncludingGravity: event.accelerationIncludingGravity,
//                         rotationRate: event.rotationRate,
//                     };
//                 });
//             }
//
//             // WebGL Renderer
//             const canvas = document.createElement('canvas');
//             const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
//             if (gl) {
//                 const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
//                 userData.webglVendor = gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL);
//                 userData.webglRenderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
//             }
//
//             // Performance Data (simple example for navigation timing)
//             if (window.performance) {
//                 userData.navigationStart = performance.timing.navigationStart;
//                 userData.loadEventEnd = performance.timing.loadEventEnd;
//             }
//
//             // Memory Information (Chrome specific)
//             if (window.performance && performance.memory) {
//                 userData.memory = {
//                     jsHeapSizeLimit: performance.memory.jsHeapSizeLimit,
//                     totalJSHeapSize: performance.memory.totalJSHeapSize,
//                     usedJSHeapSize: performance.memory.usedJSHeapSize
//                 };
//             }
//
//             return userData;
//         }
//
//         console.log(gatherUserData());


