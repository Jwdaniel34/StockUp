function myFunction() {

  // Declare variables 
  var input = document.getElementById("myInput");
  var filter = input.value.toUpperCase();
  var table = document.getElementById("myTable");
  var trs = table.tBodies[0].getElementsByTagName("tr");

  // Loop through first tbody's rows
  for (var i = 1; i < trs.length; i++) {

    // define the row's cells
    var tds = trs[i].getElementsByTagName("td");

    // hide the row
    trs[i].style.display = "none";

    // loop through row cells
    for (var i2 = 0; i2 < tds.length; i2++) {


      // if there's a match
      var firstCol = tds[0].textContent.toUpperCase();
      var secondCol = tds[1].textContent.toUpperCase();
      var thirdCol = tds[2].textContent.toUpperCase();
      if (firstCol.indexOf(filter) > -1 || secondCol.indexOf(filter) > -1 || thirdCol.indexOf(filter) > -1) {

        // show the row
        trs[i].style.display = "";

        // skip to the next row
        continue;

      }
    }
  }

}

var price = JSON.parse(document.getElementById('ts_price').textContent);
var dates = JSON.parse(document.getElementById('ts_dates').textContent);
var ctx = document.getElementById('myPortfolio').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: dates,
        datasets: [{
            label: 'Gains on Investment',
            data: price,
            lineTension: 0.3,
            backgroundColor: "rgba(60, 186, 159, 0.05)",
            borderColor: "#3cba9f",
            pointRadius: 3,
            pointBackgroundColor: "#3cba9f",
            pointBorderColor: "#3cba9f",
            pointHoverRadius: 3,
            pointHoverBackgroundColor: "#3cba9f",
            pointHoverBorderColor: "#3cba9f",
            pointHitRadius: 10,
            pointBorderWidth: 2,
        }]
    },
    options: {
        responsive: true,
        legend: {
                    display: false
                },
          maintainAspectRatio: false,
          layout: {
            padding: {
              left: 10,
              right: 25,
              top: 30,
              bottom: 0
            }
          },
        title: { display: false,
                text: 'Porfolio Investment Gains'},
        scales: {
            xAxes: [{
                stacked: false,
                ticks: {
                        display: false,
                        maxTicksLimit: 7,
                        padding: 30,
                        
                        },
              gridLines: {
                        display: false,
                        drawBorder: false
                         },
                    }]
            ,yAxes: [{
              ticks: {
                stepSize: 10,
                beginAtZero: false,
                // Include a dollar sign in the ticks
                callback: function(value, index, values) {
                    return '$' + value.toFixed(price);},
                  gridLines: {
                  color: "rgb(234, 236, 244)",
                  zeroLineColor: "rgb(234, 236, 244)",
                  drawBorder: false,
                  borderDash: [2],
                  zeroLineBorderDash: [2]
                }
              }
           }],
            tooltips: {
            backgroundColor: "rgb(255,255,255)",
            bodyFontColor: "#858796",
            titleMarginBottom: 10,
            titleFontColor: '#6e707e',
            titleFontSize: 14,
            borderColor: '#dddfeb',
            borderWidth: 1,
            xPadding: 13,
            yPadding: 13,
            displayColors: false,
            intersect: false,
            enabled: true,
            mode: 'index',
            caretPadding: 10,
          }
        },
      }
});
