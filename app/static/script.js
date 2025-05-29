document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("city");
    const datalist = document.getElementById("cities");

    let timeout = null;

    input.addEventListener("input", () => {
        clearTimeout(timeout);
        const query = input.value;

        if (query.length < 2) return;

        timeout = setTimeout(() => {
            fetch(`https://geocoding-api.open-meteo.com/v1/search?name=${encodeURIComponent(query)}&count=5`)
                .then(res => res.json())
                .then(data => {
                    datalist.innerHTML = "";
                    (data.results || []).forEach(place => {
                        const option = document.createElement("option");
                        option.value = place.name;
                        datalist.appendChild(option);
                    });
                });
        }, 300);
    });
});
