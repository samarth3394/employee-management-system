function loadPayroll() {
    fetch("http://127.0.0.1:8000/payroll/")
        .then(response => response.json())
        .then(data => {
            document.getElementById("output").textContent =
                JSON.stringify(data, null, 2);
        })
        .catch(error => {
            console.error("Error:", error);
        });
}
