// Function to toggle dark mode
const MY_SERVER = "http://127.0.0.1:8000";
let myToken = "";

const variable = sessionStorage.getItem("token")
if (variable)
    myToken = variable

let myDetails = {}
const details = sessionStorage.getItem("userDetails")
if (details) {
    myDetails = JSON.parse(details)
    const loginid = document.getElementById("loginnav")
    if (loginid) {
        loginid.remove();
        mainnav.innerHTML += 
        `
        <li class="nav-item">
            <a class="nav-link" onclick="Logout()"style="cursor: pointer;">Logout</a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="profile.html">Profile</a>
        </li>`
    }
    if (myDetails.is_staff) {
        const mainnav = document.getElementById("mainnav")
        if (mainnav) {
            mainnav.innerHTML += `
            <li class="nav-item">
                <a class="nav-link" href="management/admin.html">Admin</a>
            </li>`
        }
    }
}

function Logout(){
    if (!myToken) return
    sessionStorage.removeItem("token")
    sessionStorage.removeItem("userDetails")
    window.location.href = 'index.html';
}

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
    localStorage.setItem("darkmode", isDarkMode)
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

DarkMode()

function Message(message, type) {

    // If type not selected play a default color
    if (!type) {
        type = "linear-gradient(to right, #00b09b, #96c93d)"
    } else if (type == "error") {
        type = "linear-gradient(to right, #F74141, #B30000)"
    } else if (type == "info") {
        type = "linear-gradient(to right, #25A9F6, #0067CE)"
    } else if (type == "success") {
        type = "linear-gradient(to right, #00A510, #167e21)"
    }
    Toastify({
        text: message,
        style: {
            background: type, // Customize the background color
        },
        className: "custom-toastify", // Add a custom CSS class for styling
        position: "bottom-center", // Change the position of the notification
        duration: 3000, // Duration in milliseconds
        gravity: "top", // Change the direction of the notification animation
    }).showToast();
}