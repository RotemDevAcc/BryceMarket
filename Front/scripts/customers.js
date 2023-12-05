let retusers = {}
document.addEventListener('DOMContentLoaded', function () {
    fetch(`${MY_SERVER}/umanagement/`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${myToken}`,
        },
    })
        .then(response => response.json())
        .then(data => {
            // Call function to render user cards
            renderUserCards(data);
        })
        .catch(error => console.error('Error fetching user data:', error));
});

function renderUserCards(users) {
    retusers = users
    updateResults();
}



// Example functions for edit and delete actions

//$('#edituserModal').modal('hide');

function GetUser(userID){
    const foundUser = retusers.find(user => user.id === userID);
    return foundUser ? foundUser : null;
}

function toggleStaff(userID,set){
    const user = GetUser(userID)
    if(!user){
        Message("User Not Found","error")
        return
    }
    let setdata = {
        "userid":userID,
        "set": set
    }
    fetch(`${MY_SERVER}/umanagement/set/`,{
        method: 'PUT',
        headers: {
            'Authorization': `Bearer ${myToken}`,
        },
        body: JSON.stringify(setdata),
    })
        .then(response => response.json())
        .then(data => {
            if(data.success){
                Message(data.message,"success")
            }else{
                Message(data.message,"error")
            }
        })
}

function editUser(userID) {
    const user = GetUser(userID)
    if(!user){
        Message("User Not Found","error")
        return
    }
    const modal = new bootstrap.Modal(document.getElementById('edituserModal'));
    const detailList = document.getElementById('detailList');
    detailList.innerHTML = "";
    const listItem = document.createElement('li');
    listItem.className = 'list-group-item';
    const staffbutton = user.is_staff ? `<button class="btn btn-warning" onclick="toggleStaff(${user.id},${false})">Remove Staff</button>`:`<button class="btn btn-success" onclick="toggleStaff(${user.id},${true})">Set Staff</button>`

    listItem.innerHTML = ` You Are Editing<br>
        <strong>Username:</strong> ${user.username}<br>
        <strong>Email:</strong> ${user.email}<br>
        <strong>Staff:</strong> ${user.is_staff}<br>${staffbutton}
    `;
    detailList.appendChild(listItem);
    console.log(`Edit user with ID ${user.id}`);
    modal.show()

}

function deleteUser(userID) {
    console.log(`Delete user with ID ${userID}`);
    let setdata = {
        "userid":userID,
    }
    fetch(`${MY_SERVER}/umanagement/delete/`,{
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${myToken}`,
        },
        body: JSON.stringify(setdata),
    })
        .then(response => response.json())
        .then(data => {
            if(data.success){
                Message(data.message,"success")
            }else{
                Message(data.message,"error")
            }
        })
}

function userReceipts(userid) {
    fetch(`${MY_SERVER}/umanagement/receipts/${userid}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${myToken}`,
        },
    })
        .then(response => response.json())
        .then(data => {
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

    displayReceipts(data.receipts, allproducts)
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
            <strong>Price:</strong> $${numberWithCommas(receipt.price)}<br>
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
            <i class="fas fa-shopping-cart"></i> Product Name: ${GetProductName(product.item, allproducts)}<br>
            <i class="fas fa-box"></i> Count: ${product.count}<br>
            <i class="fas fa-dollar-sign"></i> Price: $${product.price}<br>
            `;
        return listItem.outerHTML;
    });

    return productItems.join('');
}

function GetProductName(productId, allproducts) {
    const foundProduct = allproducts.find(product => product.id === Number(productId));
    return foundProduct ? foundProduct.name : 'Product Not Found';
}

function updateResults() {
    if (!retusers || !retusers.length) return;

    const searchInput = document.getElementById("searchInput");
    const resultsList = document.getElementById("userList");

    // Get the search query
    const query = searchInput.value.toLowerCase();

    // Use array.filter to filter the data based on the query
    const filteredData = retusers.filter(user => user.username.toLowerCase().includes(query));

    // Clear previous results
    resultsList.innerHTML = "";

    // Display the filtered results

    filteredData.forEach(user => {
        const cardHtml = `
            <div class="card mb-3">
                <div class="card-body">
                    <h5 class="card-title">${user.id} - ${user.username}</h5>
                    <p class="card-text">${user.email}</p>
                    <p class="card-text">${user.firstname || "John"} ${user.lastname || "Doe"}</p>
                    <button class="btn btn-primary" onclick="editUser(${user.id})">Edit</button>
                    <button class="btn btn-danger" onclick="deleteUser(${user.id})">Delete</button>
                    <button class="btn btn-success" onclick="userReceipts(${user.id})">Receipts</button>
                </div>
            </div>
        `;

        // Append the card to the container
        resultsList.innerHTML += cardHtml;
    });
}
document.getElementById("searchInput").addEventListener("input", updateResults);