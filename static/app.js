const resultBox = document.getElementById("result");

function onScanSuccess(decodedText) {

    resultBox.innerHTML = "Scanning...";

    fetch("/scan", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            ticket: decodedText
        })
    })
    .then(res => res.json())
    .then(data => {

        if (data.success) {

            resultBox.innerHTML =
                "🟢 " + data.message +
                "<br>" + (data.nama || "");

        } else {

            resultBox.innerHTML =
                "🔴 " + data.message;

        }

    });

}

const html5QrCode = new Html5Qrcode("reader");

Html5Qrcode.getCameras().then(devices => {

    if (devices && devices.length) {

        html5QrCode.start(
            devices[0].id,
            {
                fps: 10,
                qrbox: 250
            },
            onScanSuccess
        );

    }

});