const home_url = "http://127.0.0.1:5000"
// const home_url = "https://ionextechsolutions.com/businessmanager"
function getMassData(){
    var url = `${home_url}/getMassData`
    fetch(url)
    .then(x=>x.json())
    .then(y=>{
        console.log(y)
        const viewUsers_screen = document.getElementById("viewUsers_screen")
        viewUsers_screen.innerHTML = ""
        var adder_btn = document.createElement("button")
        adder_btn.innerHTML = "+"
        adder_btn.addEventListener("click", ()=>{
            viewUsers_screen.style.display = "none"
            document.getElementById("addUser_screen").style.display = "flex"
        })
        viewUsers_screen.appendChild(adder_btn)
        const buttons = []
        for(let x = 0; x < y.length; x++){
            var unit_user = maker("div")
            unit_user.setAttribute("class", "unit_user")
            var username = maker("p")
            var phone = maker("p")
            username.innerHTML = `Name: ${y[x][1]}`
            phone.innerHTML = `Phone: ${y[x][2]}`
            buttons[x] =  document.createElement("button")
            if(y[x][5] === "False"){
                buttons[x].style.background = "greenyellow"
                buttons[x].innerHTML = "Activate"
                buttons[x].addEventListener("click",()=>{
                    var url = `${home_url}/controlUser`
                    fetch(url, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            "user_id": y[x][0],
                            "state": "False"
                        })
                    })
                    .then(p=>p.json())
                    .then(q=>{
                        if(q["state"] === "True"){
                            getMassData()
                            alert("Successful Transit")
                        }
                    })
                })
            }else{
                buttons[x].style.background = "tomato"
                buttons[x].innerHTML = "Deactivate"
                buttons[x].addEventListener("click",()=>{
                    var url = `${home_url}/controlUser`
                    fetch(url, {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            "user_id": y[x][0],
                            "state": "True"
                        })
                    })
                    .then(p=>p.json())
                    .then(q=>{
                        if(q["state"] === "True"){
                            getMassData()
                            alert("Successful Transit")
                        }
                    })
                })
            }
            unit_user.appendChild(username)
            unit_user.appendChild(phone)
            unit_user.appendChild(buttons[x])
            viewUsers_screen.appendChild(unit_user)
        }
        })
    .catch(()=>{
        alert("Internet Connection Error!! Please Check Your internet")
    })
    }

function maker(element){
    return document.createElement(element)
}

function back(){
    const x = document.getElementById("viewUsers_screen")
    x.style.display = "flex"
    document.getElementById("addUser_screen").style.display = "none"
}

// setInterval(()=>{
//     getMassData()
// }, 20000)