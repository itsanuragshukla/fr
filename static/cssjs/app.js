// Set constraints for the video stream
var constraints = { video: { facingMode: "user" }, audio: false };
var track = null;
var imgBlob;
// Define constants
const cameraView = document.querySelector("#camera--view"),
    cameraOutput = document.querySelector("#camera--output"),
    cameraSensor = document.querySelector("#camera--sensor"),
    cameraTrigger = document.querySelector("#btn3"),
    loadCamera = document.querySelector("#btn1"),
	inputDiv = document.querySelector("#inputDiv"),
	cameraDiv= document.querySelector("#cameraDiv"),
	submitDiv = document.querySelector("#submitDiv"),
	submitBtn = document.querySelector("#btn2"),
	userName = document.querySelector("#user");

function cameraStart() {
	inputDiv.classList.add('hidden');
	cameraDiv.classList.remove("hidden");
    navigator.mediaDevices
        .getUserMedia(constraints)
        .then(function(stream) {
            track = stream.getTracks()[0];
            cameraView.srcObject = stream;
        })
        .catch(function(error) {
	    alert("please make sure to allow camera permissions from your browser's settings");
            console.error("Oops. Something is broken.", error);
        });
}


cameraTrigger.onclick = async function() {
    cameraSensor.width = cameraView.videoWidth;
    cameraSensor.height = cameraView.videoHeight;
    cameraSensor.getContext("2d").drawImage(cameraView, 0, 0);
    cameraOutput.src = cameraSensor.toDataURL("image/webp");
    const blob = await (await fetch(cameraOutput.src)).blob(); 
    imgBlob=(blob);
    cameraDiv.classList.add("hidden");
    submitDiv.classList.remove("hidden");
    track.stop();
};

function submitForm(){
    var formData = new FormData(); 
    formData.append("file1", imgBlob);
    formData.append("user",userName.value);
    var request = new XMLHttpRequest();
    request.open("POST", "/");
    request.send(formData);
    //request.onreadystatechange = function() {
    //if(request.readyState == XMLHttpRequest.DONE) {
    //    var data = (request.response);
    //    console.log(data)
    //    }
    //}


fetch("/", {
        // if instead of formData, I assign requestBody to body, it works!
        body: formData,
        method: "POST",
	redirect:'follow'
    }).then(response =>{
if (response.redirected) {
            window.location.href = response.url;
        }}
)
.catch(function(err){
        console.err(err);
    });

}

submitBtn.addEventListener('click',submitForm,false);
loadCamera.addEventListener("click", cameraStart, false);
