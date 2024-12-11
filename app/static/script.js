document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".save-button").forEach(button => {
        button.addEventListener("click", function () {
            const folder = this.getAttribute("data-folder"); // Pobranie folderu z atrybutu data-folder
            const index = this.getAttribute("data-index");   // Pobranie indeksu z atrybutu data-index

            const form = document.getElementById(`save-function-${index}`);
            const formData = new FormData(form);

            // Wykonanie żądania AJAX do zapisania funkcji
            fetch("/save_function", {
                method: "POST",
                body: formData,
            })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        alert(data.message);
                    } else {
                        alert("Błąd zapisu funkcji.");
                    }
                })
                .catch(error => {
                    console.error("Wystąpił błąd:", error);
                    alert("Nie udało się zapisać funkcji.");
                });
        });
    });
});
