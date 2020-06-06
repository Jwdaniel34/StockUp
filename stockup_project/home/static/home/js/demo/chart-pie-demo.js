// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  data: {
    labels: ["Direct", "Referral", "Social"],
    datasets: [{
      data: [55, 30, 15],
      backgroundColor: ['#4e73df', '#1cc88a', '#4e73df'],
      hoverBackgroundColor: ['#2e59d9', '#17a673', '#17a673'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});

var labeled = JSON.parse(document.getElementById('Barlabels').textContent);
var barData = JSON.parse(document.getElementById('Bardata').textContent);
var colors = JSON.parse(document.getElementById('colors').textContent);
var ctx = document.getElementById('myDivChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: labeled,
        datasets: [{
            label: '# of sectors',
            data: barData,
            backgroundColor: colors,
            borderColor: colors,
            borderWidth: 1,
        }]
    },
    options: {
      maintainAspectRatio: false,
      tooltips: {
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10,
      },
      legend: {
        display: false
      },
      cutoutPercentage: 80,
    },
});

var ul = document.getElementById("labelClass");
var listItems = ul.getElementsByTagName("li");
const colored = JSON.parse(document.getElementById('colors').textContent);
var li = document.getElementById("colorchange");
var textItems = document.getElementsByClassName("sector");
for(var i = 0; i < colored.length; i++) {
listItems[i].style.color = colored[i] 
textItems[i].style.color = "black" 
}
