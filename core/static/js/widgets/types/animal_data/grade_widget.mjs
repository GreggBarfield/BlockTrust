import { Widget } from '../../widget.mjs';

export class GradeWidget extends Widget {
    constructor(frame) {
        super(frame);
    }

    initType() {
        this.account = parseInt(this.frame.getAttribute("data-widget-account"));

        this.matchType = this.frame.getAttribute("data-widget-match-type");
        this.matchStr = false;
        if (this.frame.hasAttribute("data-widget-match-str")) {
            this.matchStr = true;
        }


        this.getData(
            "get_count_distribution",
            {
                account: this.account,
                'type': this.matchType,
                'join_str': this.matchStr
            },
            (data) => {
                this.count_distribution = data.count_distribution;
            }
        );


        this.onAllDataLoaded(function () {
            this.frame.innerHTML = "";
            this.makeGraph();
        });

    }


    makeGraph() {

        this.container = document.createElement("div");
        this.container.style = "width:100%;";
        this.frame.appendChild(this.container);

        if (this.count_distribution.length == 0) {
            this.container.textContent = "(no data)";
        }
        else {
            let that = this;
            am4core.ready(function() {
                am4core.useTheme(am4themes_animated);
                var chart = am4core.create(that.container, am4charts.PieChart);

                chart.data = that.count_distribution;
                
                chart.innerRadius = am4core.percent(50);
                
                var pieSeries = chart.series.push(new am4charts.PieSeries());
                pieSeries.dataFields.value = "count";
                pieSeries.dataFields.category = "data";
                pieSeries.slices.template.stroke = am4core.color("#fff");
                pieSeries.slices.template.strokeWidth = 2;
                pieSeries.slices.template.strokeOpacity = 1;
                
                pieSeries.hiddenState.properties.opacity = 1;
                pieSeries.hiddenState.properties.endAngle = -90;
                pieSeries.hiddenState.properties.startAngle = -90;
                
            });
        }
    }
}