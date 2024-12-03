document.addEventListener("DOMContentLoaded", function() {
    console.log("Admin panel üçün xüsusi script daxil edildi!");

    // Axtarış inputu üçün debounce funksiya
    const searchInput = document.querySelector("input[name='search']");
    if (searchInput) {
        searchInput.addEventListener("input", function() {
            clearTimeout(this.searchTimeout);
            this.searchTimeout = setTimeout(() => {
                this.form.submit(); // Formu avtomatik göndər
            }, 500); // Gecikmə (500 ms)
        });
    }
});
