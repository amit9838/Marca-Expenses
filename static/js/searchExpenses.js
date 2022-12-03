const searchField = document.getElementById("searchField");
const appTable = document.getElementsByClassName("app-table")[0];
const paginationConainer = document.getElementsByClassName("pagination-container")[0];
const searchResults = document.getElementsByClassName("search-results")[0];
const home_graph = document.getElementsByClassName("home-graph")[0];

searchResults.style.display = "none";
appTable.style.display = "block";
paginationConainer.style.display = "flex";
home_graph.style.visibility = "visble";

searchField.addEventListener('keyup', (e)=> {
    appTable.style.display = "none";
    paginationConainer.style.display = "none";
    home_graph.style.visibility = "hidden";
    const searchVal = e.target.value;
    
    if(searchVal.trim().length>0) {
        // console.log(searchVal);
        results = '';
        fetch("/search-expense/", {
            body:JSON.stringify({searchText:searchVal}),
            method :"POST",
        }).then((res) =>res.json()).then((data)=> {

            // console.log("data",data);
            if(data.length === 0) {
                searchResults.style.display = "block";
                searchResults.innerHTML = "No results found"
            }
            else {
                searchResults.style.display = "block";
                

                
                data.forEach(item => {
                    const itemsID = item.id;
                    editExp = "edit-expense/attr/".replace('attr',itemsID);
                    deleteExp = "delete-expense/attr/".replace('attr',itemsID);
                    
                    let link =  function() {
                        document.location.href = deleteExp;
                        document.location.href = deleteExp;
                    }

                    
                    results += 
                           ` 
                                <tr>
                                        <td>${item.amount}</td>
                                        <td>${item.category}</td>
                                        <td>${item.description}</td>
                                        <td>${item.date}</td>
                                        <td>
                                        <div class = "float-right d-flex" style = "justify-content: center;" >
                                                <a href = "${editExp}" class = 'btn btn-secondary btn-sm mx-2' >Edit</a>
                                                <a href = "${deleteExp}" class = 'btn btn-danger btn-sm' >Delete</a>
                                            </div>
                                            </td>
                                            </tr>`;

                        });

                        let tbody =  ` 
                        <i> Showning results for <strong> </i>" ${searchVal} </strong>" . . .
                        <table class="table table-striped table-sm table-hover">
                            <thead>
                                <tr>
                                    <th scope="col">Amount</th>
                                    <th scope="col">Category</th>
                                    <th scope="col">Description</th>
                                    <th scope="col">Date</th>
                                    <th scope="col" class = "float-right d-flex" style = "justify-content: center;">Action</th>
                                    </tr>
                                </thead>
                            <tbody class="search-results-body">
                                ${results}
                            </tbody>
                        </table>`

                    searchResults.innerHTML = tbody;
                 }
        });
    }
    else {
        appTable.style.display = "block";
        paginationConainer.style.display = "flex";
        searchResults.style.display = "none";
        home_graph.style.visibility = "visible";
    }
});
