const toggleButton = document.getElementById("toggleSidebar");
const sidebar = document.querySelector(".sidebar");

if (localStorage.getItem("sidebarCollapsed") === null) {
    localStorage.setItem("sidebarCollapsed", true); 
}
if (localStorage.getItem("sidebarCollapsed") === "true") {
    sidebar.classList.add("collapsed");
}

toggleButton.addEventListener("click", function () {
    sidebar.classList.toggle("collapsed");
    localStorage.setItem("sidebarCollapsed", sidebar.classList.contains("collapsed"));
});

document.addEventListener("click", function (event) {
    if (!sidebar.contains(event.target) && !toggleButton.contains(event.target)) {
        sidebar.classList.add("collapsed");
        localStorage.setItem("sidebarCollapsed", true);
    }
});