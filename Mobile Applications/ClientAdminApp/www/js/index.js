// const home_url = "https://ionextechsolutions.com/businessmanager"
const home_url = "http://127.0.0.1:5000"
const dashscreen = document.getElementById("dashScreen")
const loginScreen = document.getElementById("loginScreen")
const productsScreen = document.getElementById("productsScreen")
const addProductScreen = document.getElementById("addProductScreen")
const logScreen = document.getElementById('logScreen')
const addUserScreen = document.getElementById('addUser')
const loading_screen = document.getElementById("loading_screen")
const add_files_screen = document.getElementById("add_files_screen")
const add_file_form = document.getElementById("add_file_form")
const updateProducts_screen = document.getElementById("updateProducts_screen")
const product_details_screen = document.getElementById("product_details_screen")
const view_employees_screen = document.getElementById("view_employees_screen")
const allScreens = [dashscreen, loginScreen, productsScreen, addProductScreen, logScreen, addUserScreen, add_files_screen, add_file_form, updateProducts_screen, product_details_screen, view_employees_screen]
// console.log(localStorage.getItem("user_id"))

var all_businesses = []
var all_products = []

function killAllScreens(){
    allScreens.forEach(element=>{
        element.style.display = "none"
    })
}

function screenManager(screen_no){
    killAllScreens()
    if(screen_no === 4){
        allScreens[screen_no].style.display = "grid"
    }else{
        allScreens[screen_no].style.display = "flex"
    }
}

function login(){
    const login_form = document.forms["login_cred"]
    if(login_form["username"].value.length === 0 || login_form["password"].value.length === 0){
        alert("Please enter a username and password")
        return
    }
    var url = `${home_url}/userLogin`
    var options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "username": login_form["username"].value,
            "password": login_form["password"].value
        })
    }
    loading_screen.style.display = "flex"
    fetch(url, options)
    .then(x=>x.json())
    .then(y=>{
        console.log(y)
        loading_screen.style.display = "none"
        if(y["state"] === "True"){
            localStorage.setItem("user_id", y["user_id"])
            getMassUnits(true)
            screenManager(0)
        }else if(y["state"] === "invalid"){
            alert("Faild Login !!!")
        }else{
            alert("Account Locked!!!-Call: 0795359098")
        }
    })
    .catch(()=>{
        alert("Please check your internet Connection")
        loading_screen.style.display = "none"
    })
}

function newUnit(){
    var data = prompt("Add New Business Unit")
    var url = `${home_url}/addNewUnit`
    var options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "user_id": localStorage.getItem("user_id"),
            "unit_name": data
        })
    }
    if(!data){
        alert("User Cancled: Name Min 3 Characters")
        return
    }
    loading_screen.style.display = "flex"
    fetch(url, options)
    .then(x=>x.json())
    .then(y=>{
        loading_screen.style.display = "none"
        if(y["state"]==="True"){
            alert("Successful Transit")
            getMassUnits(true)
        }else{
            alert("Account Locked!!!..Call: 0795359098")
        }
    })
    .catch(()=>{
        alert("Please check your internet Connection")
    })
}

function getMassUnits(state){
    var url = `${home_url}/getMassUnits`
    var options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "user_id": localStorage.getItem("user_id")
        })
    }
    if(state){
        loading_screen.style.display = "flex"
    }
    fetch(url, options)
    .then(x=>x.json())
    .then(y=>{
        loading_screen.style.display = "none"
        console.log(y)
        if(y["state"]==="invalid"){
            screenManager(1)
            return
        }
        y = y["data"]
        const userUnits = document.getElementById("userUnits")
        userUnits.innerHTML = ""
        const unitUnits = []
        all_businesses = []
        for(let x = 0; x < y.length; x++){
            unitUnits[x] = document.createElement('div')
            unitUnits[x].setAttribute("class", "unitUnit")
            unitUnits[x].addEventListener("click", ()=>{
                localStorage.setItem("unit_id", y[x][1])
                getUnitProducts(y[x][1], true)
                screenManager(2)
            })
            all_businesses.push({
                "name": y[x][2],
                "domElement": unitUnits[x]
            })
            var start_letter = document.createElement('p')
            start_letter.innerHTML =  y[x][2].charAt(0)
            var name = document.createElement('span')
            name.innerHTML = y[x][2]
            unitUnits[x].appendChild(start_letter)
            unitUnits[x].appendChild(name)
            userUnits.appendChild(unitUnits[x])
        }
        
    })
    .catch(()=>{
        if(state){
            alert("Please check your internet Connection")
        }
        console.log(state)
        loading_screen.style.display = "none"
        screenManager(1)
    })
}

function getUnitProducts(unit_id, state){
    localStorage.setItem("current_business_id", unit_id)
   var url = `${home_url}/getUnitProducts`
   var options = {
    method: "post",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        "user_id": localStorage.getItem("user_id"),
        "unit_id": unit_id
    })
   } 
   if(state){
    loading_screen.style.display = "flex"
    }
   fetch(url, options)
   .then(x=>x.json())
   .then(y=>{
    loading_screen.style.display = "none"
    console.log(y)
    const AllProducts = document.getElementById('AllProducts')
    AllProducts.innerHTML = ""
    var search_letters = document.createElement("div")
    search_letters.setAttribute("class", "search_letters")
    var letters = "#ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    var let_btns = []
    for(let r = 0; r <letters.length; r++){
        let_btns[r] = document.createElement("button")
        let_btns[r].innerHTML = letters[r]
        let_btns[r].addEventListener("click", ()=>{
            if(letters[r] == "#"){
                ProductSearch("")
            }else{
                ProductSearch(letters[r])
            }
        })
        search_letters.appendChild(let_btns[r])
    }
    AllProducts.appendChild(search_letters)
    const unit_products = []
    all_products = []
    for(let x = 0; x < y.length; x++){
        unit_products[x] = document.createElement("div")
        unit_products[x].setAttribute("class", "unitProduct")
        unit_products[x].addEventListener("click", ()=>{
            localStorage.setItem("current_product_id", y[x][2])
            screenManager(9)
            var edit_product_img = document.getElementById("edit_product_img")
            edit_product_img.src = y[x][5]
            var img_details = document.getElementById("img_details")
            img_details.src = y[x][5]
            var edit_product_name = document.getElementById("edit_product_name")
            edit_product_name.value = y[x][3]
            var view_product_name = document.getElementById("view_product_name")
            view_product_name.innerHTML = y[x][3]
            var view_product_price = document.getElementById("view_product_price")
            view_product_price.innerHTML = `Kes ${y[x][4]}`
            var edit_product_price = document.getElementById("edit_product_price")
            edit_product_price.value = y[x][4]
            var edit_product_quantity = document.getElementById("edit_product_quantity")
            edit_product_quantity.value = y[x][8]
            var view_product_stock = document.getElementById("view_product_stock")
            view_product_stock.innerHTML = `${y[x][8]} Units`
            var view_product_sold = document.getElementById("view_product_sold")
            view_product_sold.innerHTML = `${y[x][7]} Units`
            var view_product_assets = document.getElementById("view_product_assets")
            // view_product_assets.innerHTML = `Ksh ${y[x][6]}`
            view_product_assets.innerHTML = `Kes${parseInt(y[x][4])*parseInt(y[x][8])}`
        })
        var img = document.createElement("img")
        img.src = y[x][5]
        var name = document.createElement("p")
        name.innerHTML = `${y[x][3]} <br> Ksh ${y[x][4]} <br> Stock ${y[x][8]}`
        unit_products[x].appendChild(img)
        unit_products[x].appendChild(name)
        AllProducts.appendChild(unit_products[x])

        var search_object = {
            "name": y[x][3],
            "price": y[x][4],
            "domElement": unit_products[x]
        }
        all_products.push(search_object)
    }
    
   })
   .catch(()=>{
    if(state){
        alert("Please check your internet Connection")
    }
    
})
}

function ProductSearch(search_letter){
    var search_box = document.getElementById("product_search_box")
    search_box = search_box.value
    if(search_letter){
        search_box = search_letter
    }
    console.log(search_box)
    let x = 0
    if(search_box.length == 0){
        for(x = 0; x < all_products.length; x++){
            all_products[x]["domElement"].style.display = "flex"
        }
    }else{
        for(x = 0; x < all_products.length; x++){
            var substring = all_products[x]["name"].substring(0, search_box.length)
            console.log(substring)
            if(substring.toLowerCase() == search_box.toLowerCase()){
                all_products[x]["domElement"].style.display = "flex"
            }else{
                all_products[x]["domElement"].style.display = "none"
            }
        }
    }
}

function Businesssearch(){
    var search_box = document.getElementById("search_home")
    search_box = search_box.value
    let x = 0
    if(search_box.length == 0){
        for(x = 0; x < all_businesses.length; x++){
            all_businesses[x]["domElement"].style.display = "flex"
        }
    }else{
        for(x = 0; x < all_businesses.length; x++){
            var substring = all_businesses[x]["name"].substring(0, search_box.length)
            console.log(substring)
            if(substring.toLowerCase() == search_box.toLowerCase()){
                all_businesses[x]["domElement"].style.display = "flex"
            }else{
                all_businesses[x]["domElement"].style.display = "none"
            }
        }
    }
}

function AddProduct(event){
    event.preventDefault()
    const addProductForm = document.forms["addProductForm"]
    var name = addProductForm["productName"].value
    var price = addProductForm["productPrice"].value
    var quantity = addProductForm["productQuantity"].value
    var image = addProductForm["productImage"]
    var all_values = [name, price, quantity, image]
    for(let x = 0; x < all_values.length; x++){
        if(x == 3){
            if(all_values[x].files.length == 0){
                alert("Missing Image")
                return false
            }else{
                image = image.files[0]
            }
            continue
        }
        if(all_values[x].length == 0){
            alert(`Missing data sets @ ${x}`)
            return false
        }
    }
    var form = new FormData()
    form.append("user_id", localStorage.getItem("user_id"))
    form.append("biz_id", localStorage.getItem("unit_id"))
    form.append("image", image)
    form.append("name", name)
    form.append("price", price)
    form.append("quantity", quantity)
    var url = `${home_url}/addNewProduct`
    var options = {
        method: "POST",
        body: form
    }
    loading_screen.style.display = "flex"
    fetch(url, options)
    .then(x=>x.json())
    .then(y=>{
        loading_screen.style.display = "none"
        if(y["state"]==="True"){
            alert("Successful Transit")
            getUnitProducts(localStorage.getItem("unit_id"), false)
            screenManager(2)
        }else{
            alert("Transit Failed")
        }
    })
    
}

function display_new_img(event, display_board, resize) {
    const file = event.target.files[0];
    const reader = new FileReader();
    
    reader.onload = function(event) {
      const imgElement = display_board;
      imgElement.src = event.target.result;
      if(resize){
        imgElement.style.width = "100%"
        imgElement.style.height = "100%"
      }
    }
    
    reader.readAsDataURL(file);
}

function UnitProductUpdate(event){
    event.preventDefault()
    var unit_id = localStorage.getItem("current_business_id")
    var product_id = localStorage.getItem("current_product_id")
    var new_img = document.getElementById("edit_product_img_input")
    var new_name = document.getElementById("edit_product_name").value
    var new_price = document.getElementById("edit_product_price").value
    var new_quantity = document.getElementById("edit_product_quantity").value
    var all_values = [new_img, new_name, new_price, new_quantity]
    for (let index = 0; index < all_values.length; index++){
        if(index == 0){
            if(new_img.files.length == 0){
                new_img = null
            }else{
                new_img = new_img.files[0]
            }
            continue
        }
        if(all_values[index].length == 0){
            alert("Please confirm input validity")
            return
        }
    }
    var productUpdates = new FormData()
    productUpdates.append("user_id", localStorage.getItem("user_id"))
    productUpdates.append("biz_id", unit_id)
    productUpdates.append("product_id", product_id)
    productUpdates.append("new_img", new_img)
    productUpdates.append("new_name", new_name)
    productUpdates.append("new_price", new_price)
    productUpdates.append("new_quantity", new_quantity)
    var url = `${home_url}/updateProductData`
    var options = {
        method: "POST",
        body: productUpdates
    }
    loading_screen.style.display = "flex"
    fetch(url, options)
    .then(x=>x.json())
    .then(y=>{
        loading_screen.style.display = "none"
        if(y["state"]==="True"){
            alert("Successful Updates")
            getUnitProducts(unit_id, true)
            screenManager(2)
        }
    })
}

function deleteProduct(){
    var user_id = localStorage.getItem("user_id")
    var biz_id = localStorage.getItem("unit_id")
    var product_id = localStorage.getItem("current_product_id")
    var url = `${home_url}/deleteProduct`
    var data = {
        "user_id": user_id,
        "biz_id": biz_id,
        "product_id": product_id
    }
    var options = {
        method: "post",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }
    if(!confirm("Are you sure to delete selected item? ")){
        return
    }
    fetch(url, options)
    .then(x=>x.json())
    .then(y=>{
        console.log(y)
        if(y["state"]){
            alert("Product delete successfully")
            getUnitProducts(biz_id, false)
            screenManager(2)
        }
    })
}

function deleteBusiness(){
    var user_id = localStorage.getItem("user_id")
    var business_id = localStorage.getItem("unit_id")
    if(!confirm("Are you sure you want to delete business?")){
        return
    }
    var url = `${home_url}/deleteUnit`
    var data = {
        "user_id": user_id,
        "business_id": business_id
    }
    var options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }
    fetch(url, options)
    .then(x=>x.json())
    .then(y=>{
        console.log(y)
        if(y["state"]){
            alert("Successful Transit ...")
            getMassUnits(true)
            screenManager(0)
        }
    })
    .catch(()=>{
        alert("Please check your internet connection")
    })
}

function addUser(){
    const adduserform = document.forms["addUserForm"]
    const username = adduserform["username"]
    const password = adduserform["password"]
    console.log(username.value)
    console.log(password.value)
    if(username.value.length == 0 || password.value.length == 0){
        alert("Empty Fields Not Allowed")
        return
    }
    var url = `${home_url}/addNewUser`
    var options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "user_id": localStorage.getItem("user_id"),
            "biz_id": localStorage.getItem("unit_id"),
            "username": username.value,
            "password": password.value
        })
    }
    loading_screen.style.display = "flex"
    fetch(url, options)
    .then(x=>x.json())
    .then(y=>{
        loading_screen.style.display = "none"
        if(y["state"]==="True"){
            alert("Successfull Transit")
            fetchAllEmployees()
            screenManager(10)
        }else{
            alert("Error! User name Already Exists")
        }
    })
}

function getLogs(business_id, unit_business_id, product_id){
    var url = `${home_url}/getProductLogs`
    var options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "business_id": business_id,
            "unit_business_id": unit_business_id,
            "product_id": product_id
        })
    }
    loading_screen.style.display = "flex"
    fetch(url, options)
    .then(x=>x.json())
    .then(y=>{
        loading_screen.style.display = "none"
        console.log(y)
        if(y.length == 0){
            alert("No Stamps Yet, Wait for 24Hrs")
            return
        }
        const logScreen = document.getElementById("logScreen")
        logScreen.innerHTML = ""
        var heading = document.createElement("h3")
        heading.innerHTML = y[0][3]
        var back_img = document.createElement("img")
        back_img.addEventListener("click",()=>{
            screenManager(2)
        })
        back_img.src = "back_white_icon.png"
        heading.appendChild(back_img)
        logScreen.appendChild(heading)
        for(let x = 0; x < y.length; x++){
            var date = document.createElement('p')
            date.innerHTML = y[x][6]
            var amount = document.createElement('p')
            amount.innerHTML = `Ksh ${y[x][4]}`
            var quantity = document.createElement('p')
            quantity.innerHTML = `Units ${y[x][5]}`
            logScreen.appendChild(date)
            logScreen.appendChild(amount)
            logScreen.appendChild(quantity)
        }
        screenManager(4)
    })
}

function addNewFile(){
    const business_id = localStorage.getItem("user_id")
    const unit_business_id = localStorage.getItem("unit_id")
    var file_name = document.getElementById("file_name").value
    const doc_file = document.getElementById("new_file").files[0]
    if(file_name.length < 3 || doc_file.length == 0){
        alert("Empty fields not allowed")
        return
    }

    file_name = file_name.replace(/ /g, "_");
    console.log(file_name)
    // return
    
    var url = `${home_url}/addNewFile`
    var data = new FormData();
    data.append("business_id", business_id)
    data.append("unit_business_id", unit_business_id)
    data.append("file_name", file_name)
    data.append("doc_file", doc_file)

    var options = {
        method: "post",
        body:data
    }
    loading_screen.style.display = "flex"
    fetch(url, options)
    .then(x=>x.json())
    .then(y=>{
        console.log(y)
        loading_screen.style.display = "none"
        if(y["state"] == "True"){
            alert("Successful Transit")
            screenManager(3)
        }else{
            fetchAllFiles(false)
            screenManager(1)
        }
    })
    .catch(()=>{
        loading_screen.style.display = "None"
        alert("Please check your internet Connection")
    })

}

function fetchAllFiles(state){
    var url = `${home_url}/getFiles`
    var data = {
        "business_id": localStorage.getItem("user_id"),
        "unit_business_id": localStorage.getItem("unit_id"),
        "files": "All"
    }
    var options = {
        method:"POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }
    loading_screen.style.display = "flex"
    fetch(url, options)
    .then(x=>x.json())
    .then(y=>{
        loading_screen.style.display = "none"
        if(y["state"]=="True"){
            
            const all_files = document.getElementById("all_files")
            all_files.innerHTML = ""
            var y = y["data"]
            y = sortProducts(y)
            console.log(y)
            unit_file_imgs = []
            for(let x = 0; x < y.length; x++){
                var unit_file = document.createElement("div")
                unit_file.setAttribute("class", "unit_file")

                unit_file_imgs[x] = document.createElement("a")
                unit_file_imgs[x].href = `${home_url}/files/${y[x][2]}`
                unit_file_imgs[x].target="_blank"
                // unit_file_img.download = `${y[x][2]}`
                unit_file_imgs[x].setAttribute("class", "unit_file_img")
                unit_file_imgs[x].addEventListener("click", ()=>{
                    var url = `${home_url}/resetFileKey`
                    var options = {
                        method:"post",
                        headers:{
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            "file_key": y[x][2]
                        })
                    }
                    setTimeout(()=>{
                        fetch(url, options)
                        .then(x=>x.json())
                        .then(y=>{
                            console.log(y)
                            if(y["state"]){
                                unit_file_imgs[x].href = `${home_url}/files/${y["new_file_key"]}`
                            }else{

                            }
                        })
                    }, 3000)
                })
                // unit_file_imgs[x].addEventListener("onmousedown", ()=>{
                //     console.log("hello")
                // })

                var file_type_img = document.createElement("img")
                
                var file_extension = y[x][3].split(".")[1]
                if(file_extension == "jpeg" || file_extension == "jpg" || file_extension == "png" || file_extension == "PNG"){
                    file_type_img.src = "img/image.png"
                }else if(file_extension == "pdf"){
                    file_type_img.src = "img/docx.png"
                }else if(file_extension == "txt"){
                    file_type_img.src = "img/docx.png"
                }else{
                    file_type_img.src = "img/no_files_mode.png"
                }

                unit_file_imgs[x].appendChild(file_type_img)

                var unit_base = document.createElement("div")
                unit_base.setAttribute("class", "unit_base")

                var base_img = document.createElement("img")
                base_img.src = "img/folder.png"

                var file_name = document.createElement("p")
                file_name.innerHTML = `${y[x][3]} <br> ${y[x][6].split(" ")[0]}`
                
                unit_base.appendChild(base_img)
                unit_base.appendChild(file_name)

                unit_file.appendChild(unit_file_imgs[x])
                unit_file.appendChild(unit_base)

                all_files.appendChild(unit_file)
            }
        }
    })

    if(state){
        screenManager(6)
    }
    
}

function fetchAllEmployees(){
    var user_id = localStorage.getItem("user_id")
    var biz_id = localStorage.getItem("unit_id")
    var url = `${home_url}/getEmployees`
    var data = {
        "business_id": localStorage.getItem("user_id"),
        "unit_business_id": localStorage.getItem("unit_id"),
    }
    var options = {
        method:"POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }
    loading_screen.style.display = "flex"
    fetch(url, options)
    .then(x=>x.json())
    .then(y=>{
        console.log(y)
        loading_screen.style.display = "none"
        if(y["state"]){
            var display_board = document.getElementById("all_employees")
            var children = display_board.children
            for(let x = 0; x < children.length; x++){
                if(x == 0){
                    continue
                }
                children[x].style.display = "none"
            }
            var unit_employees = []
            for(let x = 0; x < y["data"].length; x++){
                unit_employees[x] = document.createElement("div")
                unit_employees[x].setAttribute("class", "unit_employee")
                unit_employees[x].addEventListener("click", ()=>{
                    console.log("lllll")
                    localStorage.setItem("employee_id", y["data"][x][2])
                    var emplyee_assets = document.getElementById('emplyee_assets')
                    emplyee_assets.innerHTML = `Ksh ${y["data"][x][4]}`
                    var employee_name = document.getElementById('employee_name')
                    employee_name.value = y["data"][x][3]
                    var employee_pass = document.getElementById('employee_pass')
                    employee_pass.value = "*** Hidden ***"
                })
                var employee_img = document.createElement("img")
                employee_img.src = "Andrelly.jpg"
                var name = document.createElement("p")
                name.innerHTML = y["data"][x][3]
                unit_employees[x].appendChild(employee_img)
                unit_employees[x].appendChild(name)
                display_board.appendChild(unit_employees[x])
            }
        }
    })
    .catch(()=>{
        alert("Please check your internet conection !!")
        loading_screen.style.display = "none"
    })
}

function updateClientDetails(state){
    if(state){
        var employee_name = document.getElementById("employee_name")
        var employee_pass = document.getElementById("employee_pass")
        if(employee_name.value.length == 0 || employee_pass.value.length == 0){
            alert("Missing data sets ...")
            return
        }
        if(employee_pass.value == "*** Hidden ***"){
            employee_pass = false
        }else{
            employee_pass = employee_pass.value
        }
        var url = `${home_url}/updateEmployee`
        var data = {
            "state": state,
            "user_id": localStorage.getItem("user_id"),
            "biz_id": localStorage.getItem("unit_id"),
            "employee_id": localStorage.getItem("employee_id"),
            "employee_name": employee_name.value,
            "employee_pass": employee_pass
        }
        var options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }
        loading_screen.style.display = "flex"
        fetch(url, options)
        .then(x=>x.json())
        .then(y=>{
            loading_screen.style.display = "none"
            console.log(y)
            if(y["state"]){
                alert("Successful Transit")
                fetchAllEmployees()
            }else{
                alert("Transition Failed ...")
            }
        })
    }else{
        if(confirm("Are you sure you want to delete ...")){
            var url = `${home_url}/updateEmployee`
            var data = {
                "state": false,
                "user_id": localStorage.getItem("user_id"),
                "biz_id": localStorage.getItem("unit_id"),
                "employee_id": localStorage.getItem("employee_id"),
            }
            var options = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            }
            loading_screen.style.display = "flex"
            fetch(url, options)
            .then(x=>x.json())
            .then(y=>{
                console.log(y)
                loading_screen.style.display = "none"
                console.log(y)
                if(y["state"]){
                    alert("Successful Transit")
                    fetchAllEmployees()
                }else{
                    alert("Transition Failed ...")
                }
            })
            .catch(()=>{
                alert("Please check your internet connection!")
                loading_screen.style.display = "none"
            })
        }
    }
}

function sortProducts(data){
    console.log(data)
    var key_elements = []
    data.forEach(element => {
        key_elements.push(element[3])
    });
    
    key_elements.sort()
    
    var new_data = []
    data.forEach(element => {
        var place = key_elements.indexOf(element[3])
        new_data[place] = element
    });
    
    return new_data
    
}

function LogOut(){
    localStorage.clear()
    loading_screen.style.display = "flex"
    location.reload()
}
