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


// function myFunction() {
//   var input, filter, table, tr, td, i;
//   input = document.getElementById("myInput");
//   filter = input.value.toUpperCase();
//   table = document.getElementById("myTable");
//   tr = table.getElementsByTagName("tr");
//   for (i = 0; i < tr.length; i++) {
//     td = tr[i].cells[0];
//     if (td) {
//       if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
//         tr[i].style.display = "";
//       } else {
//         tr[i].style.display = "none";
//       }
//     }
//   }
// }
// function myFunction() {
//   var input = document.getElementById("myInput");
//   var filter = input.value.toUpperCase();
//   var table = document.getElementById("myTable");
//   var tr = table.getElementsByTagName("tr");
//   for (var i = 0; i < tr.length; i++) {
//       if (tr.textContent.toUpperCase().indexOf(filter) > -1) {
//           tr[i].style.display = "";
//       } else {
//           tr[i].style.display = "none";
//       }      
//   }
// }