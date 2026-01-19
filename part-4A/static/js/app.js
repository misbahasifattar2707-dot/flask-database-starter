function createAuthor() {
    fetch('/api/authors', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name: document.getElementById('authorName').value,
            country: document.getElementById('authorCountry').value
        })
    }).then(loadData);
}

function createBook() {
    fetch('/api/books', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            title: document.getElementById('bookTitle').value,
            year: document.getElementById('bookYear').value,
            author_id: document.getElementById('bookAuthorId').value
        })
    }).then(loadData);
}

function loadData() {
    Promise.all([
        fetch('/api/authors').then(r => r.json()),
        fetch('/api/books').then(r => r.json())
    ]).then(([authors, books]) => {
        document.getElementById('output').textContent =
            "AUTHORS:\n" + JSON.stringify(authors, null, 2) +
            "\n\nBOOKS:\n" + JSON.stringify(books, null, 2);
    });
}

loadData();
