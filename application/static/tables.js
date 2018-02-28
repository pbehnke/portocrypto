$( document ).ready(function() {

  // http://www.christianmontoya.com/2008/11/14/extending-jquery-tablesorter-to-support-comma-delimited-numbers/
  // http://tablesorter.com/docs/example-parsers.html
  // + own adjustment to allow $-sign in front of fancy number and
  $.tablesorter.addParser({
    id: "fancyNumber",
    is: function(s) {
      // return /^[$0-9]*[0-9,\.]*[0-9]*/.test(s);
      return false
    },
    format: function(s) {
      return $.tablesorter.formatFloat( s.replace(/[,$]/g,'') );
    },
    type: "numeric"
  });


  $("#portf").tablesorter({
    headers: {
      1: {
          sorter:'fancyNumber'
      },
      3: {
          sorter:'fancyNumber'
      },
      4: {
          sorter:'fancyNumber'
      }
    },
    sortList: [[2,0]]
  });

  $("#allcoins").tablesorter({
    headers: {
      2: {
          sorter:'fancyNumber'
      },
      3: {
          sorter:'fancyNumber'
      },
      4: {
          sorter:'fancyNumber'
      },
      6: {
          sorter:'fancyNumber'
      }
    },
    sortList: [[0,0]]
  });


})
