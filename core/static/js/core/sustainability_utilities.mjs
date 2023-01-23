export const makeGaugeChart = (container, data, title, gaugeMin, gaugeMax) =>{
    am4core.ready(function() {
        am4core.useTheme(am4themes_animated);

        // create chart
        var chart = am4core.create(container, am4charts.GaugeChart);
        chart.innerRadius = -15;
        let label = chart.chartContainer.createChild(am4core.Label);
        label.text = title;
        label.align = "center";

        var axis = chart.xAxes.push(new am4charts.ValueAxis());
        axis.min = gaugeMin;
        axis.max = gaugeMax;
        axis.strictMinMax = true;
            
        var gradient = new am4core.LinearGradient();
        gradient.stops.push({color:am4core.color("red")});
        gradient.stops.push({color:am4core.color("#42f572")});

        axis.renderer.line.stroke = gradient;
        axis.renderer.line.strokeWidth = 15;
        axis.renderer.line.strokeLinecap = "round";
        axis.renderer.line.strokeOpacity = 0.90;

        var hand = chart.hands.push(new am4charts.ClockHand());
        hand.radius = am4core.percent(100);
        hand.startWidth = 16;
        hand.pin.radius = 8;
        hand.parent.zIndex = 100;

        // Setting an interval to display the gauge pointer transition animation instead of directly setting the gauge pointer
        setInterval(function() {
            hand.showValue(data, 1000, am4core.ease.cubicOut);
        }, 2000);
    });
}