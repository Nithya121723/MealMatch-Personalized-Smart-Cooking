document.addEventListener("DOMContentLoaded", function () {
    const imageInput = document.querySelector('input[type="file"]');
    const preview = document.createElement("img");
    const form = document.querySelector("form");
    const button = document.querySelector("button");

    preview.style.maxWidth = "300px";
    preview.style.marginTop = "20px";
    preview.style.borderRadius = "10px";
    preview.style.display = "none";

    form.appendChild(preview);

    imageInput.addEventListener("change", function (e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = "block";
            };
            reader.readAsDataURL(file);
            button.disabled = false;
        } else {
            preview.style.display = "none";
            button.disabled = true;
        }
    });
});
