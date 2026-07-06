const resultBox = document.getElementById("result");

let scanning = false;

function onScanSuccess(decodedText){

    if(scanning) return;

    scanning = true;

    resultBox.innerHTML="⏳ Processing...";

    fetch("/scan",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            ticket:decodedText.trim()
        })
    })
    .then(r=>r.json())
    .then(data=>{

        if(data.success){

            resultBox.innerHTML=
            "✅ "+data.nama;

        }else{

            resultBox.innerHTML=
            "❌ "+data.message;

        }

        setTimeout(()=>{
            scanning=false;
        },2000);

    })
    .catch(err=>{

        scanning=false;

        resultBox.innerHTML=err;

    });

}

// INIT QR SCANNER
const html5QrCode = new Html5Qrcode("reader");

const config = {
    fps: 10,
    qrbox: 250,
    rememberLastUsedCamera: true
};

// START CAMERA (AUTO BEST CAMERA)
Html5Qrcode.getCameras().then(devices => {

    if (!devices || devices.length === 0) {
        resultBox.innerHTML = "❌ Kamera tidak ditemukan";
        return;
    }

    let cameraId = devices[0].id;

    html5QrCode.start(
        cameraId,
        config,
        onScanSuccess
    ).then(() => {

        resultBox.innerHTML = "📷 Kamera aktif, siap scan QR";

    }).catch(err => {

        resultBox.innerHTML =
            "❌ Kamera gagal: " + err;

    });

}).catch(err => {
    resultBox.innerHTML = "❌ Error akses kamera: " + err;
});

