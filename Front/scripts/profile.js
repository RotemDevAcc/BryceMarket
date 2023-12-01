

let userName = "";
let profilePicture = "";
let email = "";



function Init() {
    if (!myDetails.user) {
        profileheader.innerHTML = `You must be logged in to use this page
        <a class="nav-link" href="index.html">Click Here</a>`;
        return
    }

    userName = myDetails.user
    email = myDetails.email
    profilePicture = myDetails.img || "placeholder.png"
    const fullname = myDetails.firstname+" "+myDetails.lastname

    profileheader.innerHTML = `Welcome ${fullname} To Your Profile<br>
    Choose Your Actions:`


    profileList.innerHTML += `
        <h3>Your Picture</h3>
        <div class="card" style="width: 18rem;">
            <img src="${MY_SERVER}/static/images/${profilePicture}" id ="profilepic" class="card-img-top" alt="Profile Picture">
            <div class="card-body">
                <h5 class="card-title">${userName}</h5>
                <button class="btn btn-primary" onclick="newPicture()">Change Picture</button>
            </div>
        </div>
    `;

    profileList.innerHTML += `
        <h3>Other: </h3>
        <div>
            <button id="receiptButton" class="btn btn-success" onclick="ShowReceipts()">My Receipts</button>
            <ul>
                <li><i class="fas fa-user"></i> Username: ${userName}</li>
                <li><i class="fas fa-envelope"></i> Email: ${myDetails.email}</li>
                <li><i class="fas fa-calendar-alt"></i> Date Of Birth: ${myDetails.dob}</li>
                <li><i class="fas fa-venus-mars"></i> Gender: ${myDetails.gender}</li>
                <li><i class="fas fa-id-card"></i> Fullname: ${fullname}<br><button class="btn btn-primary" onclick="newName()">Change Name</button></li>
            </ul>
            
        </div>
    `;

    if (myDetails.is_staff) {

    }


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

function ShowReceipts(){
    fetch(`${MY_SERVER}/profile/`,{
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${myToken}`,
        },
    })
    .then(response => response.json())
    .then(data=>{
        displayReceiptsModal(data);
    })
}

function displayReceiptsModal(data) {
    const modal = new bootstrap.Modal(document.getElementById('receiptModal'));
    const receiptContent = document.getElementById("receiptContent");

    // Clear previous content
    receiptContent.innerHTML = "";

    let allproducts = data.combdata.products
    let allcategories = data.combdata.categories

    displayReceipts(data.receipts,allproducts)
    // Create a div for each receipt in the modal content
    // data.receipts.forEach(receipt => {
    //     const receiptDiv = document.createElement("div");
    //     receiptDiv.innerHTML = `<p>Receipt ID: ${receipt.id}</p>
    //                             <p>Products: ${receipt.products}</p>
    //                             <p>Price: $${receipt.price}</p>
    //                             <hr>`;
    //     receiptContent.appendChild(receiptDiv);
    // });

    // Show the modal
    modal.show();
}

function displayReceipts(receipts, allproducts) {
    const receiptList = document.getElementById('receiptList');
    receiptList.innerHTML = "";

    receipts.forEach(receipt => {
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item';
        listItem.innerHTML = `
            <strong>Receipt ID:</strong> ${receipt.id}<br>
            <strong>Price:</strong> $${receipt.price}<br>
            <strong>Products:</strong>
            <ul>
                ${formatProducts(JSON.parse(receipt.products), allproducts)}
            </ul>
        `;
        receiptList.appendChild(listItem);
    });
}

function formatProducts(products, allproducts) {
    const productItems = products.map(product => {
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item';
        listItem.innerHTML = `
        <i class="fas fa-shopping-cart"></i> Item: ${GetProductName(product.item, allproducts)}<br>
        <i class="fas fa-box"></i> Count: ${product.count}<br>
        <i class="fas fa-dollar-sign"></i> Price: $${product.price}<br>
        `;
        return listItem.outerHTML;
    });

    return productItems.join('');
}

function GetProductName(productId, allproducts) {
    const foundProduct = allproducts.find(product => product.id === productId);
    return foundProduct ? foundProduct.name : 'Product Not Found';
}


function newName(){
    $('#changeNameModal').modal('show');
}

function submitNameForm(){
    const fullname = (myDetails && myDetails.firstname+" "+myDetails.lastname) || "None"
    const firstname = document.getElementById('changeNameFirst').value;
    const lastname = document.getElementById('changeNameLast').value;

    if (!firstname || !lastname){
        Message("Firstname And Lastname must be specified","error")
        return
    }

    const fakename = `${firstname} ${lastname}`

    if(fakename == fullname){
        Message("Your New Name cant be the same as your current name.","error")
        return
    }

    const formData = new FormData();
    formData.append('firstname', firstname);
    formData.append('lastname', lastname);
    formData.append('rtype', "newname");
    $('#changeNameModal').modal('hide');
    fetch(`${MY_SERVER}/profile/`,{
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${myToken}`,
        },
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            Message(data.message, "success");
            if(data.firstname && data.lastname){
                myDetails.firstname = data.firstname
                myDetails.lastname = data.lastname
                sessionStorage.setItem("userDetails", JSON.stringify(myDetails));
                Message(`Name Changed To: ${firstname} ${lastname}, Refresh The Page to see it.`)
            }
        } else {
            Message(data.message, "error");
        }
    })
    .catch(error => {
        Message("Couldn't change your name.", "error");
        console.error('Error:', error);
    });
}

function newPicture(){
    $('#changeImgModal').modal('show');
}

function submitPicForm(){
    if(!myToken) return window.location.href = 'index.html';
    const imageInput = document.getElementById('changeImgImage');
    const imageFile = imageInput.files[0];
    if (!imageFile) {
        Message("An image was not provided.", "error");
        return;
    }

    // Check file format and size
    const allowedFormats = ['.png'];
    const maxSize = 2 * 1024 * 1024; // 2MB

    // Validate file format based on allowedFormats
    const isValidFormat = allowedFormats.some(format => imageFile.name.toLowerCase().endsWith(format));

    if (!isValidFormat) {
        Message("Please upload a PNG image.", "error");
    } else if (imageFile.size > maxSize) {
        Message("Image size must be less than 2MB.", "error");
    } else {
        // Use fetch or other methods to send the form data to the server

        // After submitting, close the modal
        $('#changeImgModal').modal('hide');
    }

    reader.readAsArrayBuffer(imageFile);

    const formData = new FormData();
    formData.append('img', imageFile);
    formData.append('rtype', "newpicture");
    fetch(`${MY_SERVER}/profile/`,{
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${myToken}`,
        },
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            Message(data.message, "success");
            if(data.picname){
                myDetails.img = data.picname
                profilepic.src = `${MY_SERVER}/static/images/${data.picname}`
                sessionStorage.setItem("userDetails", JSON.stringify(myDetails));
            }
        } else {
            Message(data.message, "error");
        }
    })
    .catch(error => {
        Message("Couldn't Change The Picture.", "error");
        console.error('Error:', error);
    });

}

const darkModeButton = document.getElementById("darkModeButton");
darkModeButton.addEventListener("click", toggleDarkMode);