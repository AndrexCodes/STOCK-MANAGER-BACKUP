const dashProducts = document.getElementById("dashProducts")
const loginScreen = document.getElementById("loginScreen")
const loading_screen = document.getElementById("loading_screen")
const add_files_screen = document.getElementById("add_files_screen")
const add_file_form = document.getElementById("add_file_form")


const all = [dashProducts, loginScreen, add_files_screen, add_file_form]
// const home_url = "https://ionextechsolutions.com/businessmanager"
const home_url = "http://127.0.0.1:5000"

var cart_items = []
// var unit_cart_item = {
//     "business_id": business_id,
//     "unit_business_id": unit_business_id,
//     "product_id": product_id,
//     "employee_id": localStorage.getItem("employee_id"),
//     "quantity": 1,
//     "img_url": img_url,
//     "product_name": product_name,
//     "product_price": itemm_price
// }
var all_products = []
var unit_product = {
    "name": "",
    "tag": ""
}

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
        console.log(y)
        if(y["state"]==="True"){
            localStorage.setItem("employee_id", y["user_id"])
            localStorage.setItem("user_id", y["business_id"])
            localStorage.setItem("unit_biz_id", y["unit_business_id"])
            // Uncommet the bottom line fot TCP Connection - Receipt printing
            SocketConnection() // New update to fetch receipts from server over a TCP Connection
            // fetchReceipts() // Old way of HHTTP Streaming to fetch receipts from server 
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
    data = sortProducts(data)
    const products = document.getElementById("products")
    const btn_imgs = []
    all_products = []
    for(let x = 0; x < data.length; x++){
        var unit_product = document.createElement("div")
        unit_product.setAttribute("class", "unitProduct")
        btn_imgs[x] = document.createElement("img")
        btn_imgs[x].src = data[x][5]
        btn_imgs[x].addEventListener("click",()=>{
            sellProduct(data[x][0], data[x][1], data[x][2], data[x][3], data[x][4], data[x][5])
            console.log("shaudiw")
        })
        var details_container = document.createElement("div")
        var name = document.createElement('p')
        name.innerHTML = data[x][3]
        var price = document.createElement('p')
        price.innerHTML = `KES ${data[x][4]}`
        var instock = document.createElement('p')
        if(data[x][8] === "0"){
            instock.innerHTML = `OUT OF STOCK`
            instock.style.color = "red"
            instock.style.fontWeight = "900"
        }else{
            instock.innerHTML = `STOCK ${data[x][8]}`
            instock.style.color = "rgb(0, 255, 0)"
            instock.style.fontWeight = "900"
        }
        var sell_btn = document.createElement("button")
        sell_btn.innerHTML = "Add to Cart"
        unit_product.appendChild(btn_imgs[x])
        details_container.appendChild(name)
        details_container.appendChild(price)
        details_container.appendChild(sell_btn)
        details_container.appendChild(instock)
        unit_product.appendChild(details_container)
        products.appendChild(unit_product)

        var unit_product_search = {
            "name": data[x][3],
            "tag": unit_product
        }
        all_products.push(unit_product_search)

    }
    
}

function DeleteCartItem(product_id){
    for(let x = 0; x < cart_items.length; x++){
        if(cart_items[x]["product_id"] === product_id){
            cart_items.splice(x, 1);
        }
    }
    PopulateCart()
}

function PopulateCart(){
    var cart_display_board = document.getElementById("selling_cart_items")
    cart_display_board.innerHTML = ""
    var del_btns = []
    var width_size = "50%"
    var total_display = document.getElementById("cart_total")
    var total_amount = 0
    for(let x = 0; x < cart_items.length; x++) {
        var unit_cart_item = document.createElement("div")
        unit_cart_item.setAttribute("class", "unit_cart")

        var item_img = document.createElement("img")
        item_img.src = cart_items[x]["img_url"]

        var item_name = document.createElement("p")
        item_name.innerHTML = `${cart_items[x]["product_name"]}`
        item_name.style.width = width_size
        var item_price = document.createElement("p")
        item_price.innerHTML = `Price: ${cart_items[x]["product_price"]}`
        item_price.style.width = width_size
        var item_total = document.createElement("p")
        item_total.innerHTML = `Total: ${parseInt(cart_items[x]["product_price"])*parseInt(cart_items[x]["quantity"])}`
        item_total.style.width = width_size
        var quantity = document.createElement("p")
        quantity.innerHTML = `${cart_items[x]["quantity"]} Units`
        del_btns[x] = document.createElement("button");
        del_btns[x].innerHTML = 'Delete'
        del_btns[x].addEventListener("click", ()=>{
            DeleteCartItem(cart_items[x]["product_id"])
        })

        total_amount += parseFloat(parseInt(cart_items[x]["product_price"])*parseInt(cart_items[x]["quantity"]))
        unit_cart_item.appendChild(item_img)
        unit_cart_item.appendChild(item_name)
        unit_cart_item.appendChild(item_price)
        unit_cart_item.appendChild(item_total)
        unit_cart_item.appendChild(quantity)
        unit_cart_item.appendChild(del_btns[x])

        cart_display_board.appendChild(unit_cart_item)
    }
    total_display.innerHTML = `Ksh ${total_amount}.00`
    // cart_display_board.scrollTop = cart_display_board.scrollHeight
}

function sellProduct(business_id, unit_business_id, product_id, product_name, unit_price, img_url){

    let x = 0
    var add_state = true
    for(x = 0; x < cart_items.length; x++){
        console.log(cart_items[x]["product_id"] === product_id)
        if(cart_items[x]["product_id"] === product_id){
            cart_items[x]["quantity"] += 1
            add_state = false
            break
        }
    }

    if(add_state){
        var unit_cart_item = {
            "business_id": business_id,
            "unit_business_id": unit_business_id,
            "product_id": product_id,
            "employee_id": localStorage.getItem("employee_id"),
            "quantity": 1,
            "img_url": img_url,
            "product_name": product_name,
            "product_price": unit_price
        }
        cart_items.push(unit_cart_item)
    }
    PopulateCart()

}

function ConfirmSale(){
    var url = `${home_url}/ProcessSales_2`
    loading_screen.style.display = "flex"
    if(cart_items.length === 0){
        alert("No Items Selected to Cart !!")
        loading_screen.style.display = "none"
        return
    }
    data = {
        "business_id": localStorage.getItem("user_id"),
        "unit_business_id": localStorage.getItem("unit_biz_id"),
        "product_id": cart_items.map(item => item["product_id"]),
        "employee_id": localStorage.getItem("employee_id"),
        "quantity": cart_items.map(item => item["quantity"])
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
        loading_screen.style.display = "none"
        if(y["state"] === "True"){
            alert(`Successfull Sale\n Thank you\n Message: \n${y["message"]}`)
            activateReceipt()
        }else if (y["state"] === "insufficient"){
            alert(`Error!! Sales Unsuccessful ....\n The sales are more than the remaining Quantity:`)
        }
        else{
            alert("Error!! Sales Unsuccessful ....")
            alert("Error!! Sales Unsuccessful ....")
            alert("Error!! Sales Unsuccessful ....")
        }
    })
    .catch(()=>{
        loading_screen.style.display = "none"
        alert("Please Check Internet Connection ....")
        alert("Sale was Unsuccessful ....")
    })

    var cart_display_board = document.getElementById("selling_cart_items")
    cart_display_board.innerHTML = ""
    var cart_total = document.getElementById("cart_total")
    cart_total.innerHTML = "Ksh 0.00"
    cart_items = []
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
        cart_items = []
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
    
    return data
    
}

function FilterProducts(){
    var search_box = document.getElementById("product_filter")
    var text = search_box.value.toLowerCase()
    for(let x = 0; x < all_products.length; x++){
        var name = all_products[x]["name"].toLowerCase()
        var names = name.split(' ')
        for(let y = 0; y < names.length; y++){
            if(names[y].startsWith(text)){
                all_products[x]["tag"].style.display = "flex"
                break
            }else{
                all_products[x]["tag"].style.display = "none"
            }
        }
    }
    // alert(all_products.length)
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
                    file_type_img.src = "image.png"
                }else if(file_extension == "pdf" || file_extension == "txt"){
                    file_type_img.src = "docx.png"
                }else{
                    file_type_img.src = "no_files_mode.png"
                }

                unit_file_imgs[x].appendChild(file_type_img)

                var unit_base = document.createElement("div")
                unit_base.setAttribute("class", "unit_base")

                var base_img = document.createElement("img")
                base_img.src = "folder.png"

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

function fetchReceipts(){
    var url = `${home_url}/getReceipt`
    var data = {
        "business_id": localStorage.getItem("user_id"),
        "unit_business_id": localStorage.getItem("unit_biz_id")
    }
    fetch(url, setOptions(data))
    .then(x=>x.json())
    .then(y=>{
        console.log(y)
        if(y["state"]){
            data = y["data"]
            receipt_id = data[2]
            products = JSON.parse(data[3])
            receipt_date = data[5]
            PrintReceipt([receipt_id, products, receipt_date, business_name])
        }
        fetchReceipts()
    })
    .catch(()=>{
        alert("Failed to Connect to Remote Server !!")
    })
}

function PrintReceipt(data){
    var url = "http://127.0.0.1:5555/printing"
    var data = {
        "print_details": data
    }
    fetch(url, setOptions(data))
}

function setOptions(data){
    return {
        method: "post",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }
}


// Testing socket io -----------------------------------------------

function SocketConnection(){
    business_id = localStorage.getItem("user_id")
    unit_business_id = localStorage.getItem("unit_biz_id")
    var socket = io.connect(`http://127.0.0.1:5000?business_id=${business_id}&unit_business_id=${unit_business_id}`);
    socket.on('connect', function() {
        console.log('Connected');
    });

    socket.on('disconnect', function() {
        console.log('Disconnected');
    });

    function sendMessage() {
        var message = document.getElementById('message').value;
        socket.emit('message', message);
    }

    socket.on('message', function(data) {
        y = JSON.parse(data.message)
        console.log(y);
        data = y
        receipt_id = data[2]
        products = JSON.parse(data[3])
        receipt_date = data[5]
        business_name = "Not Set"
        PrintReceipt([receipt_id, products, receipt_date, business_name])
    });
}


// New navigation bar functions
function LogOut(){
    loading_screen.style.display = "flex"
    setTimeout(()=>{
        localStorage.clear()
        location.reload();
    }, 3000)
}
