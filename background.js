chrome.runtime.onInstalled.addListener(() => {
    chrome.alarms.create("dailyUpdate", {
        delayInMinutes: 1, // Start after 1 minute
        periodInMinutes: 1440, // Repeat every 24 hours
    });
});

chrome.alarms.onAlarm.addListener(async (alarm) => {
    if (alarm.name === "dailyUpdate") {
        const today = new Date().toISOString().split("T")[0];

        try {
            const response = await fetch("http://localhost:5000/update", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ startDate: today, endDate: today }),
            });

            console.log("Daily update completed.");
        } catch (error) {
            console.error("Error during daily update:", error);
        }
    }
});
