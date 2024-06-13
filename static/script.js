document.getElementById('theme-select').addEventListener('change', function() {
    const selectedTheme = this.value;
    document.documentElement.className = selectedTheme;
});


function loadTables() {
    fetch('/tables')
        .then(response => response.json())
        .then(data => {
            const tablesList = document.getElementById('tables');
            tablesList.innerHTML = '';
            data.tables.forEach(table => {
                const li = document.createElement('li');

                const selectButton = document.createElement('button');
                selectButton.textContent = table;
                selectButton.addEventListener('click', () => {
                    document.getElementById('sql-editor').value = `SELECT * FROM ${table};`;
                });
                li.appendChild(selectButton);

                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Delete';
                deleteButton.addEventListener('click', () => {
                    if (confirm(`Are you sure you want to delete the table ${table}?`)) {
                        fetch('/delete_table', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded',
                            },
                            body: 'table_name=' + encodeURIComponent(table)
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.status === 'success') {
                                alert('Table deleted successfully');
                                loadTables();
                            } else {
                                alert('Error deleting table: ' + data.error);
                            }
                        });
                    }
                });
                li.appendChild(deleteButton);

                const updateButton = document.createElement('button');
                updateButton.textContent = 'Update';
                updateButton.addEventListener('click', () => {
                    const setClause = prompt('Enter the SET clause (e.g., column1 = value1, column2 = value2)');
                    const whereClause = prompt('Enter the WHERE clause (e.g., column = value)');
                    if (setClause && whereClause) {
                        fetch('/update_table', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded',
                            },
                            body: 'table_name=' + encodeURIComponent(table) + '&set_clause=' + encodeURIComponent(setClause) + '&where_clause=' + encodeURIComponent(whereClause)
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.status === 'success') {
                                alert('Table updated successfully');
                            } else {
                                alert('Error updating table: ' + data.error);
                            }
                        });
                    }
                });
                li.appendChild(updateButton);

                tablesList.appendChild(li);
            });
        });
}

document.getElementById('execute-button').addEventListener('click', function() {
    var command = document.getElementById('sql-editor').value;
    fetch('/execute', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'command=' + encodeURIComponent(command)
    })
    .then(response => response.json())
    .then(data => {
        var resultDiv = document.getElementById('result');
        if (data.status === 'success') {
            if (data.result.columns.length > 0) {
                var table = '<table><thead><tr>';
                data.result.columns.forEach(col => {
                    table += `<th>${col}</th>`;
                });
                table += '</tr></thead><tbody>';
                data.result.rows.forEach(row => {
                    table += '<tr>';
                    row.forEach(cell => {
                        table += `<td>${cell}</td>`;
                    });
                    table += '</tr>';
                });
                table += '</tbody></table>';
                resultDiv.innerHTML = table;
            } else {
                resultDiv.innerHTML = '<pre>No data returned</pre>';
            }
        } else {
            resultDiv.innerHTML = '<pre>' + data.error + '</pre>';
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    loadTables();
});
