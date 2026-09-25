
setTimeout(function removeFlash() {
    const element = document.querySelectorAll(".flash");
    element.forEach((flash_msg) => {
        flash_msg.remove()
    })
}, 5000);