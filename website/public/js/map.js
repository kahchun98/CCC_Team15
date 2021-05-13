window.onload = function () {
	// AJAX DOM
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {

    var data = JSON.parse(this.response);
    // make charts' variables list
    var scores_price = [];
    var scores_age = [];
    var scores_cases = [];
    for (var key in data) {
        var sent_score = data[key]["score"];
        scores_price.push({x : data[key]["price"], y : sent_score});
        scores_age.push({x : data[key]["age"], y : sent_score});
        scores_cases.push({x : data[key]["cases"], y : sent_score})
    }
    // sort-x function
    function up(a, b){//升序 increase order
        return a.x - b.x;  //decrease : b.x - a.x
    }
    // sort charts' variables list using the sort-x function
    scores_price.sort(up);
    scores_age.sort(up);
    scores_cases.sort(up);

		var chart = new CanvasJS.Chart("linechart-housing", {
			animationEnabled: true,
			theme: "light2",
			title:{
				text: "View of Covid vs wealth (median housing price)"
			},
			data: [{
				type: "line",
						indexLabelFontSize: 16,
				dataPoints: scores_price
			}]
		});
		chart.render();

		var chart2 = new CanvasJS.Chart("linechart-age", {
			animationEnabled: true,
			theme: "light2",
			title:{
				text: "View of Covid vs Median Age of Population"
			},
			data: [{
				type: "line",
						indexLabelFontSize: 16,
				dataPoints: scores_age
			}]
		});
		chart2.render();

		var chart3 = new CanvasJS.Chart("linechart-cases", {
			animationEnabled: true,
			theme: "light2",
			title:{
				text: "View of Covid vs Total number of cases (as of 10th May 2021)"
			},
			data: [{
				type: "line",
						indexLabelFontSize: 16,
				dataPoints: scores_cases
			}]
		});
		chart3.render();

	}
	//TEST THIS ON API
	xhttp.open("GET", "/getjson", true);
  xhttp.send();
	}
}
