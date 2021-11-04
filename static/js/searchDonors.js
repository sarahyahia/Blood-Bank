const searchField = document.querySelector('#searchField');
const paginationContainer = document.querySelector('.pagination-container');
const tbody = document.querySelector('.t-body');
const tableOutput = document.querySelector('.table-output');
const tableApp = document.querySelector('.app-table');
const noResults= document.querySelector('.no-results');



tableOutput.style.display = 'none';

searchField.addEventListener('keyup', (e) => {
    console.log('up')
    const searchValue = e.target.value;
    
    if (searchValue.trim().length > 0) {
        
        paginationContainer.style.display = 'none';
        tbody.innerHTML = "";
        fetch("/search-donors", {
            body: JSON.stringify({ searchText: searchValue }),
            method: "POST",
            headers : { 
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        }).then((response) => response.json())
        .then((data) => {
            tableApp.style.display = 'none';
            tableOutput.style.display = 'block';
            if (data.length > 0) {
                noResults.style.display = 'none';
                data.map((item) => {
                    tbody.innerHTML+=`
                    <tr>
                    <td><a class="txt-link" href="donor/${item.id}/">${item.name}</td>
                    <td>${item.national_id}</td>
                    <td>${item.blood_type}</td>
                    <td>${item.city}</td>
                    <td>
                        <a href="edit-donor/${item.id}" class="btn btn-secondary btn-sm">
                            Edit
                        </a>
                    </td>
                    </tr>`;
                });
            }else {
                noResults.style.display = 'block';
                tableOutput.style.display = 'none';
            }
        }).catch(error => {console.error(error);});
    }else{
        tableOutput.style.display = 'none';
        tableApp.style.display = 'block';
        paginationContainer.style.display = 'block';
        noResults.style.display='none'
    }
});