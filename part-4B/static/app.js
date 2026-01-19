document.getElementById("authorForm").addEventListener("submit", function(e) {
    e.preventDefault();
    fetch("/author/add", {
        method: "POST",
        body: new FormData(this)
    }).then(() => location.reload());
});

document.getElementById("bookForm").addEventListener("submit", function(e) {
    e.preventDefault();
    fetch("/book/add", {
        method: "POST",
        body: new FormData(this)
    }).then(() => location.reload());
});

function deleteBook(bookId) {
    if (!confirm("Delete this book?")) return;

    fetch(`/book/delete/${bookId}`, {
        method: "DELETE"
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) location.reload();
    });
}

function deleteAuthor(authorId) {
    if (!confirm("Delete this author?")) return;

    fetch(`/author/delete/${authorId}`, {
        method: "DELETE"
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) location.reload();
    });
}
