

var endpoint = 'list_expenses/'

let link = function() {
  document.location.href = endpoint
}
var defaultData = [];


function fetchData() {
  // console.log("Clicked Fetch Data Button");
  const xhr = new XMLHttpRequest();

  //open the object
  xhr.open('GET',endpoint,true);


  //optional
  xhr.onprogress = function() {
      // console.log("On Progress");
  }

  xhr.onload = function(){
      if(this.status == 200){
          data = JSON.parse(this.responseText);
          // console.log(data);
          
          makechart(data)
      }
      else {
          console.error("Couldn't fetch the data.");
      }
  }

  xhr.send();  // no parameter needed. 

  // console.log("data fetched.");
}

fetchData();


// data.labels.forEach(element => {
  //   console.log(element);
  // });
  function makechart(datanew) {
    // console.log(datanew);
    amount = []
    category = []
    dates = []
  
    for( i=0;i<Object.keys(datanew.data).length;i++) {
      amt = datanew.data[i].amount
      cat = datanew.data[i].category
      date = datanew.data[i].date
      amount.push(amt)
      category.push(cat)
      dates.push(date)
    }


    const counts = {};
    let cnt =0 
    category.forEach((x) => {
      counts[x] = (counts[x] || 0) + amount[cnt];
      cnt+=1;
    });

    // console.log(counts)
    keyLst = []
    valLst = []

    for([key,val] of Object.entries(counts)) {
      keyLst.push(key)
      valLst.push(val)
    }


    //total amount
    let tamt = 0
    for(let x =0 ;x<amount.length;x++) {
      tamt+=amount[x];
    }

    document.getElementsByClassName("totalAmt")[0].innerHTML = `${tamt}`;
   
const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: keyLst,
        datasets: [{
            label: '# of Votes',
            data: valLst,
            backgroundColor: [
                'rgba(255, 99, 132, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 206, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)',
                'rgba(153, 102, 255, 0.8)',
                'rgba(255, 159, 64, 0.8)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});



const ctx2 = document.getElementById('myChart2').getContext('2d');
const myChart2 = new Chart(ctx2, {
  type: 'line',
  data: {
        labels:dates ,
        // labels:[1,2,3,4,5,6] ,
        datasets: [{
          label: 'Spent',
          data: amount,
          fill:false,
          tension:.1,
            backgroundColor: [
                'rgba(255, 99, 132, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(160, 180, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)',
                'rgba(153, 102, 255, 0.8)',
                'rgba(230, 159, 190, 0.8)'
              ],
              borderColor: [
                'rgb(77, 119, 255 ,1)',
                'rgba(54, 162, 235, 1)',
                'rgb(77 , 119 , 200, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
              ],
              borderWidth: 2
            }]
          },
          options: {
            scales: {
            y: {
                beginAtZero: true
              }
            }
          }
        });
        
        
  }
