var tickers= JSON.parse(document.getElementById('tickersymbols').textContent);

$( function() {
  $( "#tickerssymbol" ).autocomplete({
    source: tickers
  });
} );