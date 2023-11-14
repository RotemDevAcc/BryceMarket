// Function to toggle dark mode
function toggleDarkMode() {
    const body = document.body;
    body.classList.toggle("dark-mode");
    // Toggle button color
    const darkModeButton = document.getElementById("darkModeButton");
    if (darkModeButton.classList.contains("btn-secondary")) {
        darkModeButton.classList.replace("btn-secondary", "btn-primary");
        darkModeButton.innerText = "Normal Mode"
    } else {
        darkModeButton.classList.replace("btn-primary", "btn-secondary");
        darkModeButton.innerText = "Dark Mode"
    }
    const isDarkMode = body.classList.contains("dark-mode");
    localStorage.setItem("darkmode",isDarkMode)
}

const darkModeButton = document.getElementById("darkModeButton");
darkModeButton.addEventListener("click", toggleDarkMode);

function DarkMode() {
    const darkmode = localStorage.getItem("darkmode")
    if (darkmode === "true") {
        const body = document.body;
        body.classList.toggle("dark-mode");
        const darkModeButton = document.getElementById("darkModeButton");
        if (darkModeButton.classList.contains("btn-secondary")) {
            darkModeButton.classList.replace("btn-secondary", "btn-primary");
            darkModeButton.innerText = "Normal Mode"
        } else {
            darkModeButton.classList.replace("btn-primary", "btn-secondary");
            darkModeButton.innerText = "Dark Mode"
        }
    }
}