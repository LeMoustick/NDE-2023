let counter = 0;
let img = document.getElementById('click');
let btn = document.getElementById('Easter');

btn.addEventListener('click', function() {
    counter++;
    if(counter == 3) {
        const xhr = new XMLHttpRequest();
        xhr.open("POST","http://192.168.1.63/api/easter-egg",true)
        xhr.send("easter=0");
    }
});

let btn2 = document.getElementById('btn2');

btn2.addEventListener('click', function(){
    const xhr = new XMLHttpRequest();
    xhr.open("POST","http://192.168.1.63/api/easter-egg",true)
    xhr.send("easter=1");
    }
);

let btn3 = document.getElementById('btn3');

btn3.addEventListener('click', function(){
    const xhr = new XMLHttpRequest();
    xhr.open("POST","http://192.168.1.63/api/easter-egg",true)
    xhr.send("easter=2");
})