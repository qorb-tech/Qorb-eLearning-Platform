    const realFileBtn = document.getElementById("id_posti");
    const customBtn = document.getElementById("custom-button");

    customBtn.addEventListener("click", function() {
        realFileBtn.click();
    });

    var loadFile = function(event) {
        var image = document.getElementById('output');
        image.src = URL.createObjectURL(event.target.files[0]);
    };