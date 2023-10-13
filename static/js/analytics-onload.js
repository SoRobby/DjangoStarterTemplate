const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


function getDeviceType() {
    const userAgent = navigator.userAgent || navigator.vendor || window.opera;

    // Windows Phone must come first because its UA also contains "Android"
    if (/windows phone/i.test(userAgent)) {
        return "mobile";
    }

    if (/android/i.test(userAgent)) {
        return "mobile";
    }

    // iOS detection from: http://stackoverflow.com/a/9039885/177710
    if (/iPad|iPhone|iPod/.test(userAgent) && !window.MSStream) {
        return "mobile";
    }

    // Additional checks for tablets
    if (window.innerWidth <= 800 && window.innerHeight <= 600) {
        return "tablet";
    }

    return "laptop/desktop";
}


const getOnLoadUserData = () => {
    const onLoadData = {};

    onLoadData.currentTime = new Date().toISOString();


    // Browser and System Information
    onLoadData.userAgent = navigator.userAgent;
    onLoadData.platform = navigator.platform;
    onLoadData.cpuCores = navigator.hardwareConcurrency;
    if (navigator.deviceMemory) {
        onLoadData.deviceMemory = navigator.deviceMemory;
    }
    onLoadData.preferredLanguage = navigator.language;

    // Screen & Window Information
    onLoadData.screenResolution = {
        width: screen.width,
        height: screen.height,
    };
    onLoadData.windowSize = {
        width: window.innerWidth,
        height: window.innerHeight,
    };
    onLoadData.availableScreenSize = {
        width: screen.availWidth,
        height: screen.availHeight,
    };
    onLoadData.colorDepth = screen.colorDepth;
    onLoadData.pixelDepth = screen.pixelDepth;

    // Location Data
    onLoadData.referrerURL = document.referrer;
    onLoadData.origin = window.location.origin;

    // Connection Information (may not be available on all browsers)
    if (navigator.connection) {
        onLoadData.networkInfo = {
            type: navigator.connection.effectiveType,
            downlink: navigator.connection.downlink,
            rtt: navigator.connection.rtt,
        };
    }

    // Device Capabilities & Features
    onLoadData.touchSupported = 'ontouchstart' in window;
    onLoadData.preferredLanguage = navigator.language || navigator.userLanguage;
    onLoadData.timezoneOffset = new Date().getTimezoneOffset();

    // Cookies & Storage
    // Note: This will only get the size of storage items, not their content.
    onLoadData.localStorageSize = Object.keys(localStorage).length;
    onLoadData.sessionStorageSize = Object.keys(sessionStorage).length;

    if (navigator.getBattery) {
        navigator.getBattery().then(battery => {
            onLoadData.battery = {
                level: battery.level,
                isCharging: battery.charging
            }
        });
    }

    // Determine if user is likely a bot based on the user agent string
    // Note: This is a simplistic method and may not catch all bots
    const botPatterns = [
        /bot/, /crawl/, /spider/, /slurp/, /search/, /archiver/, /archive/, /wget/, /curl/, /linkchecker/
    ];
    onLoadData.isBot = botPatterns.some(pattern => pattern.test(onLoadData.userAgent.toLowerCase()));

    // Device Type
    onLoadData.deviceType = getDeviceType();

    // WebGL Support
    const gl = document.createElement('canvas').getContext('webgl');
    if (gl) {
        onLoadData.webGLVendor = gl.getParameter(gl.VENDOR);
        onLoadData.webGLRenderer = gl.getParameter(gl.RENDERER);
    }

    // To track or not track the user
    onLoadData.doNotTrack = navigator.doNotTrack || window.doNotTrack || navigator.msDoNotTrack;

    return onLoadData;
}


console.log(getOnLoadUserData())


fetch('/analytics/onload-endpoint/', {
    method: 'POST',  // Changed to POST to send data
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
        'X-Custom-Header': 'analytics-onload',

    },
    body: JSON.stringify(getOnLoadUserData())
})
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));