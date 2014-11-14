// Demo stuff

(function($) {

  // Highlighter
  hljs.initHighlightingOnLoad();

  // Demo
  var r = new Ractive({
    el: 'demo-container',
    template: '#demo-template',
    data: {
    }
  });

  // Get contests by default
  getContest('c.title', 'United States Senate');

  // Handle search
  r.on('doSearch', function(e) {
    e.original.preventDefault();
    if (this.get('titleSearch')) {
      getContest('c.title', this.get('titleSearch'));
    }
  });

  // Get contest
  function getContest(field, search) {
    var contest_fields = ['id', 'state', 'election', 'title', 'precincts_reporting', 'total_precincts', 'percent_reporting', 'total_votes', 'seats']
    var api = 'https://premium.scraperwiki.com/xcjnkr8/irxxyd91ypv1d5c/sql/?q=[[[QUERY]]]';
    var query = "SELECT * FROM contests AS c JOIN results AS r ON c.id = r.contest_id AND c.state = r.state AND c.election = r.election WHERE [[[FIELD]]] LIKE '%[[[SEARCH]]]%' LIMIT 20";
    query = query.replace('[[[FIELD]]]', field).replace('[[[SEARCH]]]', search);

    r.set('message', '');
    r.set('isLoading', true);

    $.getJSON(api.replace('[[[QUERY]]]', encodeURIComponent(query)))
      .done(function(data) {
        var contests = {};
        r.set('isLoading', false);

        // Parse out the contests and results
        _.each(_.groupBy(data, 'contest_id'), function(d, di) {
          contests[di] = {};
          contests[di].results = [];

          _.each(d, function(r) {
            var result = {};
            _.each(r, function(v, k) {
              if (_.indexOf(contest_fields, k) >= 0) {
                contests[di][k] = v;
              }
              else {
                result[k] = v;
              }
            });

            contests[di].results.push(result);
          });

          contests[di].results = _.sortBy(contests[di].results, 'percentage').reverse();
        });

        r.set('contests', contests);
      })
      .error(function() {
        r.set('message', 'Error getting data from API.');
      });
    }

})(jQuery);
