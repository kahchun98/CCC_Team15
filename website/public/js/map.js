window.onload = function () {

var chart = new CanvasJS.Chart("linechar-housing", {
	animationEnabled: true,
	theme: "light2",
	title:{
		text: "View of Covid vs wealth (median housing price)"
	},
	data: [{
		type: "line",
				indexLabelFontSize: 16,
		dataPoints: [
			{ x: 10, y: 1245 },
			{ x: 20, y: 450 },
			{ x: 34, y: 661 },
			{ x: 40, y: 12 },
			{ x: 56, y: 136 },
			{ x: 72, y: 156 },
			{ x: 78, y: 4510 }
		]
	}]
});
chart.render();

}
