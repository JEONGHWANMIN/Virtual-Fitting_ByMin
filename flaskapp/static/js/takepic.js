/*===== MENU SHOW =====*/
const showMenu = (toggleId, navId) =>{
    const toggle = document.getElementById(toggleId),
        nav = document.getElementById(navId)
    
    if(toggle && nav){
        toggle.addEventListener('click', ()=>{
            nav.classList.toggle('show')
        })
    }
}

showMenu('nav-toggle','nav-menu')

const navLink = document.querySelectorAll('.nav__link')

function linkAction(){
    // Active link
    navLink.forEach(n => n.classList.remove('active'))
    this.classList.add('active')

    //Remove menu mobile
    const navMenu = document.getElementById('nav-menu')
    navMenu.classList.remove('show')
}

navLink.forEach(n => n.addEventListener('click', linkAction))

/*===== UPLOAD IMG =====*/
// $(document).ready(function(){ 
//     var fileTarget = $('#file'); 
//     fileTarget.on('change', function(){ // 값이 변경되면
//         var cur=$(".filebox input[type='file']").val();
//         $(".upload-name").val(cur);
//     }); 
// }); 

/*===== UPLOADED IMG =====*/
// function upload() {
//     var imgcanvas = documnet.getElementById("can");
//     var fileinput = documnet.getElementById("file");
//     var image = new SimpleImage(fileinput);
//     image.drawTo(imgcanvas);
// }
