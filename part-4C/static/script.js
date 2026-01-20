document.addEventListener("DOMContentLoaded", () => {
    loadDashboard();
    loadBooks();
});

let page = 1;
let perPage = 5;
let sort = "id";
let order = "asc";

function loadDashboard() {
    fetch("/api/dashboard")
        .then(res => res.json())
        .then(data => {
            document.getElementById("totalBooks").innerText = data.total_books;
            document.getElementById("totalAuthors").innerText = data.total_authors;
        });
}

function loadBooks() {
    fetch(`/api/books?page=${page}&per_page=${perPage}&sort=${sort}&order=${order}`)
        .then(res => res.json())
        .then(data => {
            renderBooks(data.books);
            document.getElementById("pageInfo").innerText =
                `Page ${page} of ${Math.ceil(data.total / perPage)}`;
        });
}

function renderBooks(books) {
    const tbody = document.getElementById("booksBody");
    tbody.innerHTML = "";

    books.forEach(book => {
        tbody.innerHTML += `
            <tr>
                <td>${book.id}</td>
                <td>${book.title}</td>
                <td>${book.author}</td>
                <td>${book.year || "-"}</td>
            </tr>
        `;
    });
}

function nextPage() {
    page++;
    loadBooks();
}

function prevPage() {
    if (page > 1) page--;
    loadBooks();
}

function sortBy(field) {
    if (sort === field) {
        order = order === "asc" ? "desc" : "asc";
    } else {
        sort = field;
        order = "asc";
    }
    loadBooks();
}
