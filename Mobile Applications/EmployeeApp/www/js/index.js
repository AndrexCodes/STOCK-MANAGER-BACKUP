const dashProducts = document.getElementById("dashProducts")
const loginScreen = document.getElementById("loginScreen")
const loading_screen = document.getElementById("loading_screen")
const add_files_screen = document.getElementById("add_files_screen")
const add_file_form = document.getElementById("add_file_form")

const all = [dashProducts, loginScreen, add_files_screen, add_file_form]
const home_url = "https://ionextechsolutions.com/businessmanager"
// const home_url = "http://127.0.0.1:5000"
function  killAllScreens(){
    all.forEach(element=>{
        element.style.display = "none"
    })
}

function screenManager(screen_no){
    killAllScreens()
    all[screen_no].style.display = "block"
}

function logIn(){
    const login_cred = document.forms["login_cred"]
    var username = login_cred["username"]
    var password = login_cred["password"]
    var url = `${home_url}/userLoginEmployee`
    var options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
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
            localStorage.setItem("employee_id", y["user_id"])
            localStorage.setItem("user_id", y["business_id"])
            localStorage.setItem("unit_biz_id", y["unit_business_id"])
            getAllProducts(y["products"])
            screenManager(0)
        }else{
            alert("Invalid Credentials")
        }
    })
    .catch(()=>{
        alert("Internet Connection Error!! Please Check your Internet")
        loading_screen.style.display = "none"
    })
}

function getAllProducts(data){
    // data = sortProducts(data)
    const products = document.getElementById("products")
    const btn_imgs = []
    for(let x = 0; x < data.length; x++){
        var unit_product = document.createElement("div")
        unit_product.setAttribute("class", "unitProduct")
        btn_imgs[x] = document.createElement("img")
        btn_imgs[x].src = data[x][5]
        btn_imgs[x].addEventListener("click",()=>{
            sellProduct(data[x][0], data[x][1], data[x][2], data[x][3], data[x][4])
            console.log("shaudiw")
        })
        var price = document.createElement('p')
        price.innerHTML = `${data[x][3]} <br> Ksh ${data[x][4]}`
        unit_product.appendChild(btn_imgs[x])
        unit_product.appendChild(price)
        products.appendChild(unit_product)

    }
    
}

var current_sell = ""
var sell_product_name = ""
var sell_business_id = ""
var sell_unit_busniess_id = ""
var sell_unit_price = 0
var sell_amount = 0

function sellProduct(business_id, unit_business_id, product_id, product_name, unit_price){
    const display_amount = document.getElementById("no_of_products")
    console.log(current_sell)
    if(current_sell === product_id){
        display_amount.innerHTML = `${parseInt(display_amount.innerHTML)+1}`
        sell_amount = parseInt(display_amount.innerHTML)
    }else{
        display_amount.innerHTML = 1
        current_sell = product_id
        sell_product_name = product_name
        sell_business_id = business_id
        sell_unit_busniess_id = unit_business_id
        sell_amount = 1
        sell_unit_price = parseInt(unit_price)
    }
}

function ConfirmSale(){
    var statement = `PRODUCT: ${sell_product_name}
                    Quantity: ${sell_amount} Units
                    Unit Price: ksh ${sell_unit_price}
                    Total: ksh ${sell_amount*sell_unit_price}`
    if(confirm(statement)){
        const display_amount = document.getElementById("no_of_products")
        display_amount.innerHTML = "0"
        var url = `${home_url}/ProcessSales`
        var options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "business_id": sell_business_id,
                "unit_business_id": sell_unit_busniess_id,
                "product_id": current_sell,
                "employee_id": localStorage.getItem("employee_id"),
                "quantity": sell_amount
            })
        }
        loading_screen.style.display = "flex"
        fetch(url, options)
        .then(x=>x.json())
        .then(y=>{
            if(y["state"] === "True"){
                alert("Successfull Sale\n Thank you")
                
            }else if (y["state"] === "insufficient"){
                alert("Error!! Sales Unsuccessful ....\n The sales are more than the remaining Quantity:")
            }
            else{
                alert("Error!! Sales Unsuccessful ....")
                alert("Error!! Sales Unsuccessful ....")
                alert("Error!! Sales Unsuccessful ....")
            }
            loading_screen.style.display = "none"
        })
        .catch(()=>{
            alert("Please Check Internet Connection ....")
            alert("Sale was Unsuccessful ....")
            loading_screen.style.display = "none"
        })
    }
}

function activateReceipt(){
    business_id = localStorage.getItem("user_id")
    unit_business_id = localStorage.getItem("unit_biz_id")
    employee_id = localStorage.getItem("employee_id")
    
    var url = `${home_url}/activateReceipt`
    var options = {
        method: "post",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "business_id": business_id,
            "unit_business_id": unit_business_id,
            "employee_id": employee_id
        })
    }
    fetch(url, options)
    .then(x=>x.json())
    .then(y=>{
        console.log(y)
        if(y["state"]){
            alert("Successful Printing ...")
        }
    })
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

function addNewFile(){
    const business_id = localStorage.getItem("user_id")
    const unit_business_id = localStorage.getItem("unit_biz_id")
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
        }else{
            fetchAllFiles(false)
            screenManager(2)
        }
    })
    .catch(()=>{
        alert("Please Check your internet Connection")
        loading_screen.style.display = "none"
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

                var file_type_img = document.createElement("img")
                
                var file_extension = y[x][3].split(".")[1]
                console.log(file_extension)
                if(file_extension == "jpeg" || file_extension == "jpg" || file_extension == "png"){
                    file_type_img.src = "img/image.png"
                }else if(file_extension == "pdf" || file_extension == "txt"){
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
    .catch(()=>{
        alert("Please Check your internet Connection")
        loading_screen.style.display = "none"
    })

    if(state){
        screenManager(2)
    }
    
}
