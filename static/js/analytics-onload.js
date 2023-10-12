const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


const getOnLoadUserData = () => {
    const onLoadData = {};

    onLoadData.currentTime = new Date().toISOString();
    onLoadData.userAgent = navigator.userAgent;
    onLoadData.window = {
        width: window.innerWidth,
        height: window.innerHeight,
    }
    onLoadData.preferredLanguage = navigator.language;
    onLoadData.platform = navigator.platform;
    onLoadData.referrer = document.referrer;

    return onLoadData;
}


// Collecting data

const screenResolution = `${screen.width}x${screen.height}`;


fetch('/analytics/onload-endpoint/', {
    method: 'POST',  // Changed to POST to send data
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
        'X-Custom-Header': 'Analytics',

    },
    body: JSON.stringify(getOnLoadUserData())
})
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));