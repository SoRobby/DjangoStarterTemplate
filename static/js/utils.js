// Utility Functions
// Loaded into the project at the base level in the head of the DOM.


// function convertUTCToLocalTime(utcTimeString) {
//   // Create a new Date object from the UTC string
//   const utcDate = new Date(utcTimeString + "Z");  // Append "Z" to indicate that the time is in UTC
//
//   // Convert to the local time string
//   const localTimeStr = utcDate.toLocaleString();
//
//   return localTimeStr;
// }


document.addEventListener("DOMContentLoaded", function (event) {

    document.querySelectorAll('.convert-time').forEach(element => {
        const utcDateString = element.getAttribute('data-utc-time');
        element.textContent = new Date(utcDateString).toLocaleString();
    });

});


function openFeedbackModal() {
    const feedbackButton = document.getElementById('btn-feedback');
    if (feedbackButton) {
        feedbackButton.click();
    }
}


// function convertUTCToLocalTime(utcTimeString, dateFormat, timeFormat) {
//   // Create a new Date object from the UTC string
//   const utcDate = new Date(utcTimeString + "Z");
//
//   // Initialize output strings
//   let customDate = "";
//   let customTime = "";
//
//   // Only format the date if dateFormat is provided
//   if (dateFormat) {
//     const year = utcDate.getFullYear();
//     const month = String(utcDate.getMonth() + 1).padStart(2, '0');
//     const day = String(utcDate.getDate()).padStart(2, '0');
//
//     customDate = dateFormat
//       .replace("Y", year)
//       .replace("m", month)
//       .replace("d", day);
//   }
//
//   // Only format the time if timeFormat is provided
//   if (timeFormat) {
//     const hour = String(utcDate.getHours()).padStart(2, '0');
//     const minute = String(utcDate.getMinutes()).padStart(2, '0');
//     const second = String(utcDate.getSeconds()).padStart(2, '0');
//
//     let hours = utcDate.getHours();
//     let ampm = hours >= 12 ? 'PM' : 'AM';
//     hours = hours % 12;
//     hours = hours ? hours : 12; // the hour '0' should be '12'
//     const hour12 = String(hours).padStart(2, '0');
//
//     customTime = timeFormat
//       .replace("H", hour)
//       .replace("i", minute)
//       .replace("s", second)
//       .replace("h", hour12)
//       .replace("A", ampm);
//   }
//
//   // Combine customDate and customTime, omitting any that weren't formatted
//   return [customDate, customTime].filter(Boolean).join(' ');
// }

// Usage examples


function convertUtcToLocalWithLocaleFormat(utcTimeString) {
    // Create a new Date object from the UTC string
    const utcDate = new Date(utcTimeString + "Z");  // Append "Z" to indicate that the time is in UTC

    const lang = navigator.language || navigator.userLanguage;  // Get the browser language setting

    let timeFormat;

    // Assume English-speaking countries may prefer 12-hour clock (not always accurate!)
    if (lang.startsWith("en")) {
        timeFormat = {hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true};
    } else {
        timeFormat = {hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false};
    }

    // Convert to the local time string
    let localTimeStr = utcDate.toLocaleTimeString(lang, timeFormat);

    // Format AM/PM as a.m./p.m.
    if (timeFormat.hour12) {
        localTimeStr = localTimeStr.replace("AM", "a.m.").replace("PM", "p.m.");
    }

    return localTimeStr;
}

// Usage
